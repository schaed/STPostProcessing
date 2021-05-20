import csv
import numpy as np
import os,sys
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
debug=False
#from root_numpy import root2array, tree2array
#from root_numpy import array2tree, array2root
import ROOT
import array
from operator import add
#Zee 950135 1.92
#Wmunu 950045 19915
#list( map(add, list1, list2) )
def plot(listPlotExtra, ylabel,xaxis, xlabel,fit=[]):
    ncolor=0
    color=['-b','-r','-g','-y','-p']
    for name,newList in listPlotExtra.iteritems():
        plt.plot(xaxis,newList,color[ncolor], label=name)
        ncolor+=1
    for func in fit:
        plt.plot(func[1],func[0],'-g')
    #plt.plot(xaxis,listPlot)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(loc="lower left")
    plt.show()

def DefineRewQCD(inputWeights, binning, atlasMCRatio, p=None):

    np_inputWeights=np.array(inputWeights)
    np_atlasMCRatio=np.array(atlasMCRatio)
    for b in range(0,len(inputWeights)):
        inputWeights[b][2]=atlasMCRatio[b]*(0.3*(inputWeights[b][0]-4000.0)/4000.0+0.3) # mjj slope of 0.3/4000 GeV with an uncertainty of 0.3 at 4000 GeV
        if p!=None:
            sysFrac=p(inputWeights[b][0])-1.0
            if sysFrac>0.25:
                sysFrac=0.25
            inputWeights[b][2]=atlasMCRatio[b]*sysFrac
            #print inputWeights[b][2],inputWeights[b][0],sysFrac
    #print 'inputWeights',inputWeights

def DefineRewEWK(inputWeights, binning, atlasMCRatio, p=None):

    np_inputWeights=np.array(inputWeights)
    np_atlasMCRatio=np.array(atlasMCRatio)
    for b in range(0,len(inputWeights)):
        inputWeights[b][2]=atlasMCRatio[b]*(0.02*(inputWeights[b][0]-4000.0)/4000.0+0.03)
        if p!=None:
            sysFrac=p(inputWeights[b][0])-1.0
            inputWeights[b][2]=atlasMCRatio[b]*sysFrac
            #print inputWeights[b][2],inputWeights[b][0],sysFrac
    #print 'inputWeights',inputWeights
    
def RebinToJonas(binning, my_arr):
    #print binning
    fineBin=[ x[0] for x in my_arr]
    fineBin+=[13000.0]

    newArray=[]
    j=0
    for b in binning:
        bin_sum=0.0
        while fineBin[j]<b:
            bin_sum+=my_arr[j][2]
            #print ' .... summing:',fineBin[j]
            j+=1
        if b!=500.0:
            newArray+=[bin_sum]
        #print b,fineBin[j]
    #print newArray
    return newArray
        
def WriteHist(f, my_arr, n1, WZ_atlas_corr=[], isNom=False):
    #print my_arr
    #binning = my_arr[:,0]
    binning=[ x[0] for x in my_arr]
    binning+=[13000.0]
    #print binning
    newBinning = array.array('d',binning)
    plt = ROOT.TH1F(n1,n1,len(newBinning)-1,newBinning)
    #vals = my_arr[:,2]
    vals = [ x[2] for x in my_arr]
    j=1
    isZnn = n1.count('vvj_')
    for a in vals:
        divA = a/WZ_atlas_corr[j-1]
        if isZnn:
            if isNom:
                plt.SetBinContent(j,1.0)
            else:
                plt.SetBinContent(j,0.0)                
        else:
            plt.SetBinContent(j,divA)
        j+=1
    f.cd()
    plt.SetDirectory(f)
    plt.Write()
    
#with open('testfile.csv', newline='') as csvfile:
#    data = list(csv.reader(csvfile))

#print(data)
corr_R = np.genfromtxt('R_mjj_nominal.csv', delimiter=' ')
binning=[ x[0] for x in corr_R]
binning+=[10000.0]
midpoints = binning[:-1]+(np.diff(binning)/2.0)
print 'midpoints: ',midpoints
print 'binning: ',binning
cjv='_cjv'
cjv=''
# derive the atlas corrections
Znn_atlas = np.genfromtxt('strongYodas/Znn_atlas'+cjv+'.csv', delimiter='\t')
Wmn_atlas = np.genfromtxt('strongYodas/Wmnu_atlas'+cjv+'.csv', delimiter='\t')
cjvapp='_cjv'
Znn_atlas_cjv = np.genfromtxt('strongYodas/Znn_atlas'+cjvapp+'.csv', delimiter='\t')
Wmn_atlas_cjv = np.genfromtxt('strongYodas/Wmnu_atlas'+cjvapp+'.csv', delimiter='\t')

##
cjvapp=''
HTPrimeZnn_atlas = np.genfromtxt('strongYodas/HTPrime/Znn_atlas'+cjv+'.csv', delimiter='\t')
HTPrimeWmn_atlas = np.genfromtxt('strongYodas/HTPrime/Wmnu_atlas'+cjv+'.csv', delimiter='\t')
cjvapp='_cjv'
HTPrimeZnn_atlas_cjv = np.genfromtxt('strongYodas/HTPrime/Znn_atlas'+cjvapp+'.csv', delimiter='\t')
HTPrimeWmn_atlas_cjv = np.genfromtxt('strongYodas/HTPrime/Wmnu_atlas'+cjvapp+'.csv', delimiter='\t')
##
#cjv=''
Znn_EWK_atlas = np.genfromtxt('ewkYodas/Znn_EWK'+cjv+'_atlas.csv', delimiter='\t')
Wmn_EWK_atlas = np.genfromtxt('ewkYodas/Wmn_EWK'+cjv+'_atlas.csv', delimiter='\t')
Wen_EWK_atlas = np.genfromtxt('ewkYodas/Wen_EWK'+cjv+'_atlas.csv', delimiter='\t')

Znn_EWK_atlas_cjv = np.genfromtxt('ewkYodas/Znn_EWK'+cjvapp+'_atlas.csv', delimiter='\t')
Wmn_EWK_atlas_cjv = np.genfromtxt('ewkYodas/Wmn_EWK'+cjvapp+'_atlas.csv', delimiter='\t')
Wen_EWK_atlas_cjv = np.genfromtxt('ewkYodas/Wen_EWK'+cjvapp+'_atlas.csv', delimiter='\t')

Znn_rebin = RebinToJonas(binning, Znn_atlas)
Wmn_rebin = RebinToJonas(binning, Wmn_atlas)
HTPrimeZnn_rebin = RebinToJonas(binning, HTPrimeZnn_atlas)
HTPrimeWmn_rebin = RebinToJonas(binning, HTPrimeWmn_atlas)
Znn_EWK_rebin = RebinToJonas(binning, Znn_EWK_atlas)
Wmn_EWK_rebin = RebinToJonas(binning, Wmn_EWK_atlas)
Wen_EWK_rebin = RebinToJonas(binning, Wen_EWK_atlas)

Znn_rebin_cjv = RebinToJonas(binning, Znn_atlas_cjv)
Wmn_rebin_cjv = RebinToJonas(binning, Wmn_atlas_cjv)
HTPrimeZnn_rebin_cjv = RebinToJonas(binning, HTPrimeZnn_atlas_cjv)
HTPrimeWmn_rebin_cjv = RebinToJonas(binning, HTPrimeWmn_atlas_cjv)
Znn_EWK_rebin_cjv = RebinToJonas(binning, Znn_EWK_atlas_cjv)
Wmn_EWK_rebin_cjv = RebinToJonas(binning, Wmn_EWK_atlas_cjv)
Wen_EWK_rebin_cjv = RebinToJonas(binning, Wen_EWK_atlas_cjv)

# Try summing EWK+QCD
np_Znn_EWK_rebin=np.array(Znn_EWK_rebin)
np_Wmn_EWK_rebin=np.array(Wmn_EWK_rebin)
np_Wen_EWK_rebin=np.array(Wen_EWK_rebin)
np_Wln_EWK_rebin=np_Wen_EWK_rebin+np_Wmn_EWK_rebin
np_Wln_EWK_rebin/=2.0
np_Znn_QCD_rebin=np.array(Znn_rebin)
np_Wmn_QCD_rebin=np.array(Wmn_rebin)
np_Znn_QCDEWK_rebin = np_Znn_EWK_rebin+np_Znn_QCD_rebin
np_Wmn_QCDEWK_rebin = np_Wln_EWK_rebin+np_Wmn_QCD_rebin

# cjv versions
np_Znn_EWK_rebin_cjv=np.array(Znn_EWK_rebin_cjv)
np_Wmn_EWK_rebin_cjv=np.array(Wmn_EWK_rebin_cjv)
np_Wen_EWK_rebin_cjv=np.array(Wen_EWK_rebin_cjv)
np_Wln_EWK_rebin_cjv=np_Wen_EWK_rebin_cjv+np_Wmn_EWK_rebin_cjv
np_Wln_EWK_rebin_cjv/=2.0
np_Znn_QCD_rebin_cjv=np.array(Znn_rebin_cjv)
np_Wmn_QCD_rebin_cjv=np.array(Wmn_rebin_cjv)
np_Znn_QCDEWK_rebin_cjv = np_Znn_EWK_rebin_cjv+np_Znn_QCD_rebin_cjv
np_Wmn_QCDEWK_rebin_cjv = np_Wln_EWK_rebin_cjv+np_Wmn_QCD_rebin_cjv
np_Znn_QCD_rebin_cjv/=np_Wmn_QCD_rebin_cjv
np_Znn_QCD_rebin_cjv/=3.0
np_Znn_EWK_rebin_cjv/=np_Wln_EWK_rebin_cjv
np_Znn_EWK_rebin_cjv/=3.0

#HTPrime
np_HTPrimeZnn_QCD_rebin=np.array(HTPrimeZnn_rebin)
np_HTPrimeWmn_QCD_rebin=np.array(HTPrimeWmn_rebin)
np_HTPrimeZnn_QCD_rebin_cjv=np.array(HTPrimeZnn_rebin_cjv)
np_HTPrimeWmn_QCD_rebin_cjv=np.array(HTPrimeWmn_rebin_cjv)
np_HTPrimeZnn_QCD_rebin_cjv*=0.2
np_HTPrimeZnn_QCD_rebin*=0.2
np_HTPrimeZnn_QCD_rebin/=np_HTPrimeWmn_QCD_rebin
np_HTPrimeZnn_QCD_rebin_cjv/=np_HTPrimeWmn_QCD_rebin_cjv

#####
#Draw the ratios of W/Z
np_Znn_QCDEWK_rebin/=np_Wmn_QCDEWK_rebin
np_Znn_QCDEWK_rebin/=3.0
print np_Znn_QCDEWK_rebin
if debug:
    plot({'QCD+EWK':np_Znn_QCDEWK_rebin},'Znn/Wln QCD+EWK',midpoints,'mjj [GeV]')
np_Znn_EWK_rebin/=np_Wln_EWK_rebin
np_Znn_EWK_rebin/=3.0
if debug:
    plot({'EWK':np_Znn_EWK_rebin},'Znn/Wln EWK',midpoints,'mjj [GeV]')
np_Wen_EWK_rebin/=np_Wmn_EWK_rebin
if debug:
    plot({'EWK':np_Wen_EWK_rebin},'Wen/Wmn EWK',midpoints,'mjj [GeV]')
np_Znn_QCD_rebin/=np_Wmn_QCD_rebin
np_Znn_QCD_rebin/=3.0
if debug:
    plot({'Znn/Wln':np_Znn_QCD_rebin},'Znn/Wln QCD',midpoints,'mjj [GeV]')
print '-------'

WZ_atlas=[]
WZ_EWK_atlas=[]
for j in range(0,len(Znn_rebin)):
    r=0.0
    if Wmn_rebin[j]>0.0:
        r=Znn_rebin[j]/Wmn_rebin[j]/3.0
    WZ_atlas+=[r]
    r=0.0
    if np_Wln_EWK_rebin[j]>0.0:
        r=Znn_EWK_rebin[j]/np_Wln_EWK_rebin[j]/3.0
        print r
    WZ_EWK_atlas+=[r]
print 'WZ_atlas',WZ_atlas
print 'WZ_EWK_atlas',WZ_EWK_atlas

#TH1 *hStrongRNLO         = getHisto(fIn, process + "_QCD_R_mjj_nominal");
#TH1 *hStrongdRNLOQCD     = getHisto(fIn, process + "_QCD_dR_mjj_QCD");
#TH1 *hStrongdRNLOPS      = getHisto(fIn, process + "_QCD_dR_mjj_PS");
#TH1 *hStrongdRNLOMix     = getHisto(fIn, process + "_QCD_dR_mjj_Mix");
#TH1 *hStrongdRNLORew     = getHisto(fIn, process + "_QCD_dR_mjj_Rew");
#corr_R = np.genfromtxt('Znn_Wen_QCD.dat', delimiter=' ')
#corr_R = np.loadtxt('Znn_Wen_QCD.dat', delimiter=' ')
#corr_R = np.genfromtxt('R_mjj_nominal.csv', delimiter=' ')
dR_mjj_QCD = np.genfromtxt('dR_mjj_QCD.csv', delimiter=' ')
dR_mjj_PS  = np.genfromtxt('dR_mjj_PS.csv',  delimiter=' ')
dR_mjj_Rew = np.genfromtxt('dR_mjj_QCD.csv', delimiter=' ')
dR_mjj_Mix = np.genfromtxt('dR_mjj_QCD.csv', delimiter=' ')

# draw the ratio of theory / atlas for QCD
np_WZ_atlas = np.array(WZ_atlas)
ratio_corr_R=[ x[2] for x in corr_R]
ratio_corr_R/=np_WZ_atlas
if debug:
    plot({'no veto':ratio_corr_R},'Znn/Wln double ratio Theory / ATLAS QCD',midpoints,'mjj [GeV]')
ratio_corr_R_cjv=[ x[2] for x in corr_R]
ratio_corr_R_HTPrimecjv=[ x[2] for x in corr_R]
ratio_corr_R_HTPrime=[ x[2] for x in corr_R]
ratio_corr_R_cjv/=np_Znn_QCD_rebin_cjv
ratio_corr_R_HTPrimecjv/=np_HTPrimeZnn_QCD_rebin
ratio_corr_R_HTPrime/=np_HTPrimeZnn_QCD_rebin_cjv
if debug or True:
    plot({'Jet Veto':ratio_corr_R_cjv,'no veto':ratio_corr_R},'Znn/Wln double ratio Theory / ATLAS QCD w/cjv',midpoints,'mjj [GeV]')
    plot({'HTPrime Jet Veto':ratio_corr_R_HTPrimecjv,
              'HTPrime No Veto':ratio_corr_R_HTPrime,
              'Jet Veto':ratio_corr_R_cjv,'no veto':ratio_corr_R},'Znn/Wln double ratio Theory / ATLAS QCD w/cjv',midpoints,'mjj [GeV]')    

ratio_corr_R_cjv_sys=deepcopy(ratio_corr_R_cjv)
ratio_corr_R_cjv_sys/=ratio_corr_R

z = np.polyfit(midpoints, ratio_corr_R_cjv_sys,3)
print 'Fit paramaters QCD: ',z[0],z[1],z[2],z[3]
xp = np.linspace(midpoints[0], midpoints[-1], 100)
p = np.poly1d(z)
plot({'cjv/noveto':ratio_corr_R_cjv_sys},'Double ratio theory/ATLAS, QCD, cjv/No Veto',midpoints,'mjj [GeV]',[[p(xp),xp]])

fout = ROOT.TFile.Open('fout.root','recreate')


#print 'inputWeights',dR_mjj_Rew
# create the reweighting input for QCD
DefineRewQCD(dR_mjj_Rew, binning, WZ_atlas,p)

WriteHist(fout, corr_R,     'evj_QCD_R_mjj_nominal', WZ_atlas, isNom=True)
WriteHist(fout, dR_mjj_QCD, 'evj_QCD_dR_mjj_QCD',    WZ_atlas)
WriteHist(fout, dR_mjj_PS,  'evj_QCD_dR_mjj_PS',     WZ_atlas)
WriteHist(fout, dR_mjj_Rew, 'evj_QCD_dR_mjj_Rew',    WZ_atlas)
WriteHist(fout, dR_mjj_PS,  'evj_QCD_dR_mjj_Mix',    WZ_atlas)

WriteHist(fout, corr_R,     'vvj_QCD_R_mjj_nominal', WZ_atlas, isNom=True)
WriteHist(fout, dR_mjj_QCD, 'vvj_QCD_dR_mjj_QCD',    WZ_atlas)
WriteHist(fout, dR_mjj_PS,  'vvj_QCD_dR_mjj_PS',     WZ_atlas)
WriteHist(fout, dR_mjj_Rew, 'vvj_QCD_dR_mjj_Rew',    WZ_atlas)
WriteHist(fout, dR_mjj_PS,  'vvj_QCD_dR_mjj_Mix',    WZ_atlas)

####EWK
corr_EWK_R      = np.genfromtxt('R_EWK_mjj_nominal.csv', delimiter=' ')
dR_EWK_mjj_QCD  = np.genfromtxt('dR_EWK_mjj_QCD.csv', delimiter=' ')
dR_EWK_mjj_PS   = np.genfromtxt('dR_EWK_mjj_PS.csv', delimiter=' ')
dR_EWK_mjj_Rew  = np.genfromtxt('dR_EWK_mjj_Rew.csv', delimiter=' ')
dR_EWK_mjj_Mix  = np.genfromtxt('dR_EWK_mjj_Mix.csv', delimiter=' ')

# draw the ratio of theory / atlas for EWK
np_WZ_EWK_atlas = np.array(WZ_EWK_atlas)
ratio_corr_EWK_R=[ x[2] for x in corr_EWK_R]
ratio_corr_EWK_R/=np_WZ_EWK_atlas
if debug:
    plot({'no veto':ratio_corr_EWK_R},'Znn/Wln double ratio Theory / ATLAS EWK',midpoints,'mjj [GeV]')
ratio_corr_EWK_R_cjv=[ x[2] for x in corr_EWK_R]
ratio_corr_EWK_R_cjv/=np_Znn_EWK_rebin_cjv
if debug:
    plot({'jet veto':ratio_corr_EWK_R_cjv,'no veto':ratio_corr_EWK_R},'Znn/Wln double ratio Theory / ATLAS EWK w/cjv',midpoints,'mjj [GeV]')

ratio_corr_EWK_R_cjv_sys=deepcopy(ratio_corr_EWK_R_cjv)
ratio_corr_EWK_R_cjv_sys/=ratio_corr_EWK_R
if debug:
    plot({'cjv/noveto':ratio_corr_EWK_R_cjv_sys},'Znn/Wln double ratio Theory / ATLAS EWK w/cjv',midpoints,'mjj [GeV]')

z = np.polyfit(midpoints, ratio_corr_EWK_R_cjv_sys, 2)
print 'Fit paramaters EWK: ',z[0],z[1],z[2]
xp = np.linspace(midpoints[0], midpoints[-2], 100)
p = np.poly1d(z)

plot({'cjv/noveto':ratio_corr_EWK_R_cjv_sys},'Double ratio theory/ATLAS, EWK, cjv/No Veto',midpoints,'mjj [GeV]',[[p(xp),xp]])

# create the reweighting input for EWK
DefineRewEWK(dR_EWK_mjj_Rew, binning, WZ_EWK_atlas,p)
WriteHist(fout, corr_EWK_R,     'evj_EWK_R_mjj_nominal', WZ_EWK_atlas, isNom=True)
WriteHist(fout, dR_EWK_mjj_QCD, 'evj_EWK_dR_mjj_QCD',    WZ_EWK_atlas)
WriteHist(fout, dR_EWK_mjj_PS,  'evj_EWK_dR_mjj_PS',     WZ_EWK_atlas)
WriteHist(fout, dR_EWK_mjj_Rew, 'evj_EWK_dR_mjj_Rew',    WZ_EWK_atlas)
WriteHist(fout, dR_EWK_mjj_PS,  'evj_EWK_dR_mjj_Mix',    WZ_EWK_atlas)

WriteHist(fout, corr_EWK_R,     'vvj_EWK_R_mjj_nominal', WZ_EWK_atlas, isNom=True)
WriteHist(fout, dR_EWK_mjj_QCD, 'vvj_EWK_dR_mjj_QCD',    WZ_EWK_atlas)
WriteHist(fout, dR_EWK_mjj_PS,  'vvj_EWK_dR_mjj_PS',     WZ_EWK_atlas)
WriteHist(fout, dR_EWK_mjj_Rew, 'vvj_EWK_dR_mjj_Rew',    WZ_EWK_atlas)
WriteHist(fout, dR_EWK_mjj_PS,  'vvj_EWK_dR_mjj_Mix',    WZ_EWK_atlas)

fout.Write()
fout.Close()
#print corr_R

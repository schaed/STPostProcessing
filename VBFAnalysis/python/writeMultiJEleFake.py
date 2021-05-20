#!/usr/bin/env python
import ROOT
import os

def getMJRandSUncInputs(year, mjyield, a, doClos=True):

    tail_unc_list = [-0.246,0.062,0.054]
    core_unc_list = [0.205,-0.082,-0.061]
    aunc = 0
    if a==12: aunc=1
    elif a==13: aunc=2
    tail_unc=tail_unc_list[aunc]
    core_unc=core_unc_list[aunc]

    hist_list=[]
    histClosUp=[]
    histClosDw=[]
    for yea in [2016, 2017, 2018]:
        histClosUp += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)]
        histClosDw += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5) ]

    # rebalance and smear core variation
    histRandSCoreHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
    histRandSCoreLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
    # rebalance and smear tail variation
    histRandSTailHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJTailUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJTailUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
    histRandSTailLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJTailUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJTailUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
    # apply the systematic uncertainties
    histRandSCoreHigh.SetBinContent(1,mjyield*(1.0+core_unc))
    histRandSCoreHigh.SetBinError(1,0.0)
    histRandSCoreLow.SetBinContent(1,mjyield*(1.0-core_unc))
    histRandSCoreLow.SetBinError(1,0.0)
    histRandSTailHigh.SetBinContent(1,mjyield*(1.0+tail_unc))
    histRandSTailHigh.SetBinError(1,0.0)
    histRandSTailLow.SetBinContent(1,mjyield*(1.0-tail_unc))
    histRandSTailLow.SetBinError(1,0.0)
    # setting the default value
    for itr in range(0,len(histClosUp)):
        histClosUp[itr].SetBinContent(1,mjyield)
        histClosUp[itr].SetBinError(1,0.0)
        histClosDw[itr].SetBinContent(1,mjyield)
        histClosDw[itr].SetBinError(1,0.0)                    
        if  year==2016:
            histClosUp[0].SetBinContent(1,mjyield*1.9) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
            histClosDw[0].SetBinContent(1,mjyield/1.9)
        elif  year==2017:
            histClosUp[1].SetBinContent(1,mjyield*1.491) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
            histClosDw[1].SetBinContent(1,mjyield/1.491)
        elif  year==2018:
            histClosUp[2].SetBinContent(1,mjyield*1.371) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
            histClosDw[2].SetBinContent(1,mjyield/1.371)
    
    hist_list+=[histRandSCoreHigh,histRandSCoreLow,histRandSTailHigh,histRandSTailLow]
    if doClos:
        for c in (histClosUp+histClosDw):
            hist_list+=[c]
    return hist_list

def writeMultiJetFJVT(Binning=0, year=2016, METCut=150, doDoubleRatio=False, singleHist=False, doTMVA=False, doOneHighFJVTCR=False):
    f_multijet = ROOT.TFile("multijetFJVT.root", "recreate")
    mjs = [2.14, 1.99, 1.53, 1.38, 1.65, 1.97, 1.85, 1.67, 1.30, 1.18, 35.5]
    emjs = [0.2, 0.2, 0.2, 0.2, 0.2, 0.28, 0.26, 0.22, 0.2, 0.23, 0.36]
    statemjs = [0.10, 0.18, 0.17, 0.10, 0.27, 0.13, 0.17, 0.19, 0.25, 0.23, 0.29]        
    if Binning==11 or Binning==12 or Binning==13 or Binning==21 or Binning==22 or Binning==30 or Binning==40: # set for all years
        #mjs = [2.32, 2.03, 2.0, 1.28, 1.84, 5.87, 5.06, 5.0, 3.24, 4.66, 2.0]
        #emjs = [0.12, 0.15, 0.18, 0.32, 0.25, 0.12, 0.15, 0.18, 0.32, 0.25, 0.18] 
        #if METCut==160:
        #    mjs = [2.32, 2.03, 2.0, 1.28, 1.84, 5.87, 5.06, 5.0, 3.24, 4.66, 2.0]
        #    emjs = [0.12, 0.15, 0.18, 0.32, 0.25, 0.12, 0.15, 0.18, 0.32, 0.25, 0.18] 
        if Binning==21 or Binning==22:
            mjs = [2.29, 2.19, 1.63, 1.52, 1.82, 1.75, 1.76, 2.10, 2.35, 3.38, 30.5]
            mjs+=[18.7,3.9] # these are from the R&S
            emjs += [0.36, 0.36]
            statemjs+=[0.22, 0.42]
        if Binning==22:
            #mjs+=[1.04,0.9,0.95] # these were guesses
            #emjs += [0.1, 0.12, 0.15]
            mjs+=[0.37,0.32,0.36]
            emjs += [0.27, 0.20, 0.23]
            statemjs+=[0.1, 0.1,.18]
        if Binning==23: # drops the dphijj binning
            mjs = [2.7, 2.3, 2.3, 1.45, 2.0, 40.0, 6.6, 4.4]
            emjs = [0.12, 0.15, 0.18, 0.32, 0.25, 0.25, 0.25, 0.25 ]
            mjs+=[0.55,0.63,0.46]
            emjs += [0.10, 0.09, 0.24]

        if Binning==30 or  Binning==40: # drops the dphijj binning
            mjs = [2.7, 2.3, 2.3, 1.45, 2.0]
            emjs = [0.12, 0.15, 0.18, 0.32, 0.25]
        if Binning==40: # drops the dphijj cut and binning and 1<njet<6 for susy.
            mjs = [1.6, 1.6, 1.6, 1.6, 1.6]
            emjs = [0.12, 0.15, 0.18, 0.32, 0.25]
            
    mjshape=[]
    mjshape_staterr=[]
    mjshape_coresyserr=[]
    mjshape_tailsyserr=[]
    if doOneHighFJVTCR:
        # integral of these needs to be that of the bin 6 fjvt transfer. will be normalized later
        mjshape = [0.31238394,0.43419236,0.13576130,0.11622656,0.0014358363]
        mjshape_staterr = [0.22,0.15,0.31,0.25,0.97]
        mjshape_coresyserr = [0.10,0.09,0.08,-0.2,-0.27]
        mjshape_tailsyserr = [-0.07,0.06,0.02,0.11,0.15]        
        
    a=1
    hists=[]
    histcr=None
    hist=None
    for mj in mjs:
        histcr = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_FJVTCR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_FJVTCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        hist = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histcr.SetBinContent(1,1.0)
        histcr.SetBinError(1,0.05)
        hist.SetBinContent(1,mj)
        #hist.SetBinError(1,mj*0.07)
        hist.SetBinError(1,mj*statemjs[a-1])
        histHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"TFMJUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"TFMJUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"TFMJUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"TFMJUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histMidMETHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"TFMidMETMJUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"TFMidMETMJUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histMidMETLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"TFMidMETMJUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"TFMidMETMJUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)        
        histHigh.SetBinContent(1,mj*(1.+emjs[a-1]))
        histHigh.SetBinError(1,0.0)
        histLow.SetBinContent(1,mj*(1.-emjs[a-1]))
        histLow.SetBinError(1,0.0)
        histMidMETHigh.SetBinContent(1,mj*(1.+emjs[a-1]))
        histMidMETHigh.SetBinError(1,0.0)
        histMidMETLow.SetBinContent(1,mj*(1.-emjs[a-1]))
        histMidMETLow.SetBinError(1,0.0)        
        # these are the R&S, so remove them
        if Binning==11 and a==11:
            histcr.SetBinContent(1,0.0)
            hists+=[hist]
            hists+=getMJRandSUncInputs(year, mj, a)
        elif (Binning==21 or Binning==22) and (a==11 or a==12 or a==13):
            histcr.SetBinContent(1,0.0)
            hists+=[hist]
            hists+=getMJRandSUncInputs(year, mj, a)
        elif (Binning==21 or Binning==22) and doOneHighFJVTCR and (a>=6 and a<=10):

            # hard coding the fjvt transfer for one bin
            entrynum = a-6
            mjvalFJVT = 1.82
            total_mj_int = sum(mjshape) # total integral
            scale_factor_mj = mjvalFJVT/total_mj_int # apply this bin by bin
            mjvalone = scale_factor_mj*mjshape[entrynum]
            hist.SetBinContent(1,mjvalone)
            hist.SetBinError(1,mjvalone*0.0) # setup later to correlate correctly
            histLow.SetBinContent(1,mjvalone*0.8)
            histHigh.SetBinContent(1,mjvalone*(1.+0.2))

            # stat uncertainty on the TF is propagated to all bins
            histStatHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"TFStatMjjShapeMJUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"TFStatMjjShapeMJUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histStatLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"TFStatMjjShapeMJUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"TFStatMjjShapeMJUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histStatHigh.SetBinContent(1,1.11*mjvalone)
            histStatHigh.SetBinError(1,0.0)
            histStatLow.SetBinContent(1,(1.-0.11)*mjvalone)
            histStatLow.SetBinError(1,0.0)
            # rebalance and smear stats
            strname='one'
            if a==7: strname='two'
            if a==8: strname='thr'
            if a==9: strname='fou'
            if a==10: strname='fiv'
            histRandSStatHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"RSStat"+strname+"MJUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"RSStat"+strname+"MJUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histRandSStatLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"RSStat"+strname+"MJUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"RSStat"+strname+"MJUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histRandSStatHigh.SetBinContent(1,(1.+mjshape_staterr[entrynum])*mjvalone)
            histRandSStatHigh.SetBinError(1,0.0)
            histRandSStatLow.SetBinContent(1,(1.-mjshape_staterr[entrynum])*mjvalone)
            histRandSStatLow.SetBinError(1,0.0)
            # rebalance and smear core variation
            histRandSCoreHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histRandSCoreLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histRandSCoreHigh.SetBinContent(1,(1.+mjshape_coresyserr[entrynum])*mjvalone)
            histRandSCoreHigh.SetBinError(1,0.0)
            histRandSCoreLow.SetBinContent(1,(1.-mjshape_coresyserr[entrynum])*mjvalone)
            histRandSCoreLow.SetBinError(1,0.0)
            # rebalance and smear tail variation
            histRandSTailHigh = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJTailUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJTailUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histRandSTailLow = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJTailUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJTailUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histRandSTailHigh.SetBinContent(1,(1.+mjshape_tailsyserr[entrynum])*mjvalone)
            histRandSTailHigh.SetBinError(1,0.0)
            histRandSTailLow.SetBinContent(1,(1.-mjshape_tailsyserr[entrynum])*mjvalone)
            histRandSTailLow.SetBinError(1,0.0)
            if a!=6:
                histcr.SetBinContent(1,0.0)
                hists+=[hist,histHigh,histLow,histStatHigh,histStatLow,histRandSStatLow,histRandSStatHigh,histRandSCoreLow,histRandSCoreHigh,histRandSTailLow,histRandSTailHigh]
            else:
                hists+=[histcr,hist,histHigh,histLow,histStatHigh,histStatLow,histRandSStatLow,histRandSStatHigh,histRandSCoreLow,histRandSCoreHigh,histRandSTailLow,histRandSTailHigh]
        elif a>13:
            hists+=[histcr,hist,histMidMETHigh,histMidMETLow]
        else:  
            hists+=[histcr,hist,histHigh,histLow]
        a += 1

    f_multijet.cd()
    for h in hists:
        h.Write()
    f_multijet.Close()

def writeMultiJet(Binning=0, year=2016, METCut=150, doDoubleRatio=False, singleHist=False, doTMVA=False, doHighDphijj=False):
    multijets = [7.13, 2.24, 0.45]
    #multijets = [3.0, 0.5, 0.1]
    #multijets = [58.+3.0, 28.0+0.5, 26.0+0.1]
    if Binning==-1:
        multijets = [31.0, 14.5, 13.0, 30.0, 14.0, 13.0]
    if Binning==1:
        multijets = [3.0, 0.5, 0.1, 112.] 
    if Binning==2:
        multijets = [58.0, 27.5, 25.0, 5.0]
    if Binning==3:
        multijets = [3.0, 0.5, 0.1, 58.0, 27.0, 25.0]
    if Binning==4:
        multijets = [58.0, 27.5, 25.0, 4.0, 0.5, 0.5]
    if Binning==5:
        multijets = [31.0, 14.5, 13.0, 30.0, 14.0, 13.0]
    if Binning==6:
        multijets = [30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
        multijets += [5.0]
    if Binning==7:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
        multijets += [5.0]
    if Binning==8:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
        multijets += [5.0]
    if Binning==9:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
    if Binning==10:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 10.0, 10.0, 2.0, 2.0]
        multijets += [5.0]
    if Binning==11 or Binning==12 or Binning==13 or Binning==21 or Binning==22:
        #multijets=[88.1, 102.9, 32.3, 21.3, 1.6, 69.5, 127.1, 35.7, 23.1, 0.0,56.4]
        #multijets_statunc=[12.2, 13.2, 4.7, 5.3, 0.9, 7.0, 12.8, 5.2, 5.2, 0.2,11.1]
        multijets=[83.0,99.6,30.7,21.4,2.4,71.2,132.0,36.97,23.8,0.0,56.5]
        multijets_statunc=[24.6,29.3,8.9,10.2,2.4,13.5,21.95,10.5,8.4,0.2,11.0]
        if METCut>150:
            tmpmj=[83.0,99.6,30.7,21.4,2.4,71.2,132.0,36.97,23.8,0.0,56.5]
            tmpmj_statunc=[24.6,29.3,8.9,10.2,2.4,13.5,21.95,10.5,8.4,0.2,11.0]
            tmpmj=[71.2,132.0,36.97,23.8,0.0,83.0,99.6,30.7,21.4,2.4,56.5]
            tmpmj_statunc=[13.5,21.95,10.5,8.4,0.2,24.6,29.3,8.9,10.2,2.4,11.0]
            # these are scaled:
            tmpmj=[99.7867063926122, 119.74404767113464, 36.90905887052042, 25.72813875664941, 2.8853987390634854, 58.26565689050047, 108.02059985317503, 30.253951337665768, 19.47644148867853, 0.0, 56.5]
            tmpmj_statunc=[29.57533707540073, 35.22590960606672, 10.700020324027092, 12.262944641019812, 2.8853987390634854, 11.047561348620174, 17.96251641497873, 8.592547715593469, 6.874038172474776, 0.1636675755351137, 11.0]
            if Binning==12:
                scaleMETAngle=[0.121065412554,0.338276163341,0.52910552342,0.903512478309,1.0,0.4107]
                for i in range(0,5):
                    tmpmj[i]=tmpmj[i]*scaleMETAngle[i]
                    tmpmj[i+5]=tmpmj[i+5]*scaleMETAngle[i]
                    tmpmj_statunc[i]=tmpmj_statunc[i]*scaleMETAngle[i]
                    tmpmj_statunc[i+5]=tmpmj_statunc[i+5]*scaleMETAngle[i]
                tmpmj[10]=tmpmj[10]*scaleMETAngle[5]
                tmpmj_statunc[10]=tmpmj_statunc[10]*scaleMETAngle[5]
            multijets=[]; multijets_statunc=[];
            MJSF=0.659
            if METCut==160: 
                MJSF=0.70609
                #multijets = [66.6, 78.6, 28.7, 18.1, 1.5, 49.2, 79.6, 23.9, 21.0, 0., 27.0] # MET>150
                #multijets_statunc = [19.8,23.1,8.4,8.7,1.5,9.3,13.3,6.8,7.3,0.2,7.2]
            if METCut==165:
                MJSF=0.5434
            elif METCut==170:
                MJSF=0.4518
            elif METCut==180:
                MJSF=0.34
            elif METCut==190:
                MJSF=0.22
            elif METCut==200:
                MJSF=0.152
            for i in range(0,len(tmpmj)):
                multijets+=[(MJSF)*tmpmj[i]] # MET>160... from scaling to low mjj
                multijets_statunc+=[(MJSF)*tmpmj_statunc[i]] # MET>160... from scaling to low mjj
    # MJ for other years
    if year==2017:
        if Binning==11 or Binning==12 or Binning==13 or Binning==21 or Binning==22:
            #multijets=[166.1, 194.1, 61.0, 40.2, 3.1, 131.1, 239.7, 67.3, 43.5, 0.0,188.5]
            #multijets_statunc=[23.0, 24.9, 8.8, 10.0, 1.6, 13.2, 24.2, 9.9, 9.9, 0.2,31.2]
            multijets=[161.3,193.6,59.9,41.5,4.6,132.7,245.7,68.8,44.2,0,182.2]
            multijets_statunc=[32.8,54.9,13.6,15.2,4.6,27.2,45.4,15.9,18.6,0,32.0]
            tmpmj=[161.3,193.6,59.9,41.5,4.6,132.7,245.7,68.8,44.2,0,182.2]
            tmpmj_statunc=[32.8,54.9,13.6,15.2,4.6,27.2,45.4,15.9,18.6,0,32.0]
            tmpmj=[132.7,245.7,68.8,44.2,0,161.3,193.6,59.9,41.5,4.6,182.2]
            tmpmj_statunc=[27.2,45.4,15.9,18.6,0,32.8,54.9,13.6,15.2,4.6,32.0]
            # these are scaled
            tmpmj=[193.12220019968197, 231.79453167178195, 71.71741966497798, 49.687360869725985, 5.507514698813001, 108.14509178504075, 200.23548644750952, 56.06919604228187, 36.0211986201869, 0.0, 182.2]
            tmpmj_statunc=[39.27097437414488, 65.73099064452907, 16.283086935621043, 18.198744222164695, 5.507514698813001, 22.16689145857655, 36.999149713947624, 12.957851992329676, 15.15824195329132, 0.0, 32.0]
            if Binning==12:
                scaleMETAngle=[0.147241433143,0.309987184443,0.708798656468,0.970501756401,1.0,0.5944]
                for i in range(0,5):
                    tmpmj[i]=tmpmj[i]*scaleMETAngle[i]
                    tmpmj[i+5]=tmpmj[i+5]*scaleMETAngle[i]
                    tmpmj_statunc[i]=tmpmj_statunc[i]*scaleMETAngle[i]
                    tmpmj_statunc[i+5]=tmpmj_statunc[i+5]*scaleMETAngle[i]
                tmpmj[10]=tmpmj[10]*scaleMETAngle[5]
                tmpmj_statunc[10]=tmpmj_statunc[10]*scaleMETAngle[5]
            if METCut>150:
                multijets=[]; multijets_statunc=[];
                MJSF=0.6991
                if METCut==160:
                    MJSF=0.6991
                    #multijets= [79., 125., 51., 20.8, 2.7, 94.2, 118., 58., 13.6, 2.6, 108.2]
                    #multijets_statunc = [16.1,35.5,11.6,7.7,2.7,19.2,21.8,13.5,5.7,2.6,19.0]
                elif METCut==165: 
                    MJSF=0.62322
                elif METCut==170: 
                    MJSF=0.540
                elif METCut==180: 
                    MJSF=0.415 # 
                elif METCut==190: 
                    MJSF=0.290 # 
                elif METCut==200: 
                    MJSF=0.204 # 
                for i in range(0,len(tmpmj)):
                    multijets+=[(MJSF)*tmpmj[i]] # MET>160... from scaling to low mjj
                    multijets_statunc+=[(MJSF)*tmpmj_statunc[i]] # MET>160... from scaling to low mjj
        else:
            print 'MJ is not defined for binning: ',Binning
    elif year==2018:
        if Binning==11 or Binning==12 or Binning==13 or Binning==21 or Binning==22:
            #multijets=[210.7, 246.2, 77.3, 51.0, 3.9, 166.3, 304.0, 85.3, 55.2, 0.0, 331.0]
            #multijets_stat=[29.2, 31.6, 11.2, 12.6, 2.1, 16.7, 30.6, 12.5, 12.5, 0.2, 58.7]
            multijets=[182.1,218.5,67.6,46.8,5.2,174.5,323.1,90.5,58.2,0.0,364.3]
            multijets_statunc=[35.6,42.8,20.3,16.9,5.20,31.9,75.7,24.7,18.9,0.2,71.6]
            tmpmj=[182.1,218.5,67.6,46.8,5.2,174.5,323.1,90.5,58.2,0.0,364.3]
            tmpmj=[174.5,323.1,90.5,58.2,0.0,182.1,218.5,67.6,46.8,5.2,364.3]
            tmpmj_statunc=[35.6,42.8,20.3,16.9,5.20,31.9,75.7,24.7,18.9,0.2,71.6]
            tmpmj_statunc=[31.9,75.7,24.7,18.9,0.2,35.6,42.8,20.3,16.9,5.20,71.6]
            # these are scaled:
            tmpmj=[221.24316195217506, 265.4674952583759, 82.13090471151584, 56.8598571079725, 6.317761900885834, 144.3089941630104, 267.19906025254244, 74.84220041118877, 48.130564242333556, 0.0, 364.3]
            tmpmj_statunc=[43.25236993683379, 52.00004026113725, 24.66357049768893, 20.53272617787896, 6.317761900885834, 26.380841912894166, 62.602812940629725, 20.42654530559517, 15.630028594159864, 0.1653971279805277, 71.6]
            if Binning==12:
                scaleMETAngle=[0.204859872988,0.494068121587,0.560479833879,0.814771265068,1.0,0.734375]
                for i in range(0,5):
                    tmpmj[i]=tmpmj[i]*scaleMETAngle[i]
                    tmpmj[i+5]=tmpmj[i+5]*scaleMETAngle[i]
                    tmpmj_statunc[i]=tmpmj_statunc[i]*scaleMETAngle[i]
                    tmpmj_statunc[i+5]=tmpmj_statunc[i+5]*scaleMETAngle[i]
                tmpmj[10]=tmpmj[10]*scaleMETAngle[5]
                tmpmj_statunc[10]=tmpmj_statunc[10]*scaleMETAngle[5]
            if METCut>150:
                multijets=[]; multijets_statunc=[];
                MJSF=0.7655
                #multijets = [250., 120., 48.9, 25.3, 2.9, 260., 108., 44.3, 33.4, 0.0, 278.8] # MET>150... from scaling to low mjj
                #   multijets_statunc = [49.0,23.4,14.6,9.1,2.9,60.9,19.8,12.1,10.9,0.2,54.8]
                if METCut==160:
                    MJSF=0.7655
                elif METCut==165: 
                    MJSF=0.6634
                elif METCut==170:
                    MJSF=0.59065
                elif METCut==180:
                    MJSF=0.480 # not computed
                elif METCut==190:
                    MJSF=0.330 # not computed
                elif METCut==200:
                    MJSF=0.189 # not computed
                for i in range(0,len(tmpmj)):
                    multijets+=[(MJSF)*tmpmj[i]] # MET>160... from scaling to low mjj
                    multijets_statunc+=[(MJSF)*tmpmj_statunc[i]] # MET>160... from scaling to low mjj
        elif Binning==0:
            multijets = [400, 200, 200]
        elif Binning==6:
            multijets = [300.0, 135, 120.0, 70.0, 120.0, 120.0, 50.0]
        else:
            print 'MJ is not defined for binning: ',Binning
    # let's split njet bin and add lower met bins
    if Binning==21 or Binning==22:
        if year==2016:
            multijets[10]=4.6
            multijets_statunc[10]=2.0
            multijets+=[2.3,0.2]
            multijets_statunc+=[1.0,0.2]
            if Binning==22:
                multijets+=[24.5,18.3,0.5]
                multijets_statunc+=[3.2,4.3,0.5]
        elif year==2017:
            multijets[10]=11.6
            multijets_statunc[10]=5.2
            multijets+=[5.7,0.9]
            multijets_statunc+=[2.5,0.5]
            if Binning==22:
                multijets+=[62.0,46.4,0.8]
                multijets_statunc+=[8.1,10.9,0.8]
        elif year==2018: #set for 2018
            multijets[10]=14.3
            multijets_statunc[10]=6.4
            multijets+=[7.1,0.6]
            multijets_statunc+=[3.1,0.6]
            if Binning==22: # for 160-200. 150 to 160 efficiency is 0.67
                multijets+=[76.7,57.3,1.8]
                multijets_statunc+=[10.0,13.5,0.9]
    if doHighDphijj and (Binning==30 or Binning==40):
        multijets=[]
        multijets_statunc=[] # total 150, set for MET>160 GeV with post-CONF numbers
        if year==2016:
            multijets=[19.2054,21.9784,18.6385,13.2151,0.56133]
            multijets_statunc=[5.85454,4.30036,4.10462,3.12942,0.1]
        elif year==2017:
            multijets=[19.2054,21.9784,18.6385,13.2151,0.56133]
            multijets_statunc=[5.85454,4.30036,4.10462,3.12942,0.1]
        elif year==2018:
            multijets=[19.2054,21.9784,18.6385,13.2151,0.56133]
            multijets_statunc=[5.85454,4.30036,4.10462,3.12942,0.1]
    if doTMVA:
        #multijets=[293.3,77.9,38.2,38.7,26.7,69.9,13.7,11.9,51.6,7.1,9.1]
        #multijets_statunc=[25.,18.,12.,12.,16.,30.,7.,9.,45.,7.1,9.1]
        #multijets=[534.7,52.3,24.1,34.2,19.1,14.1,25.9,10.5,134.0,10.9,80.2]
        #multijets_statunc=[40.,18.,12.,12.,16.,30.,7.,9.,45.,7.1,9.1] # avas
        multijets=[614.7,152.3,44.1,34.2,19.1,14.1,25.9,10.5,13.0,5.9,5.2] # for george best
        multijets_statunc=[40.,18.,12.,12.,16.,30.,7.,9.,4.,2.1,2.1]

        # divide for the periods
        divideUnit=3.0
        if year==2016:   divideUnit=9.0
        elif year==2017: divideUnit=2.571428
        elif year==2018: divideUnit=2.0
        for m in range(0,len(multijets)):
            multijets[m]=multijets[m]/divideUnit
            multijets_statunc[m]=multijets_statunc[m]/divideUnit

    if doDoubleRatio:
        multijets+=[300.0]
    a = 1
    f_multijet = ROOT.TFile("multijet.root", "recreate")    
    if not singleHist:
        imult=-1
        for multijet in multijets:
            imult+=1
            hist=None
            histClosUp=[]
            histClosDw=[]
            if doDoubleRatio and a==(len(multijets)):
                hist   = ROOT.TH1F("hmultijet_antiVBFSel_1Nom_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1Nom_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
                histUp = ROOT.TH1F("hmultijet_antiVBFSel_1MJCoreUncHigh_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1MJCoreUncHigh_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
                histDw = ROOT.TH1F("hmultijet_antiVBFSel_1MJCoreUncLow_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1MJCoreUncLow_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
                for yea in [2016, 2017, 2018]:
                    histClosUp +=[ ROOT.TH1F("hmultijet_antiVBFSel_1MJClos%sUncHigh_AVBFCR1_obs_cuts" %yea, "hmultijet_VBFjetSel_1MJClos%sUncHigh_AVBFCR1_obs_cuts;;" %yea, 1, 0.5, 1.5)]
                    histClosDw +=[ ROOT.TH1F("hmultijet_antiVBFSel_1MJClos%sUncLow_AVBFCR1_obs_cuts" %yea, "hmultijet_VBFjetSel_1MJClos%sUncLow_AVBFCR1_obs_cuts;;" %yea, 1, 0.5, 1.5) ]
            else:
                hist   = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histUp = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histDw = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                for yea in [2016, 2017, 2018]:
                    histClosUp += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClosHDPhi%sUncHigh_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClosHDPhi%sUncHigh_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)]
                    histClosDw += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClosHDPhi%sUncLow_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClosHDPhi%sUncLow_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5) ]
                    histClosUp += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClosLDPhi%sUncHigh_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClosLDPhi%sUncHigh_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)]
                    histClosDw += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClosLDPhi%sUncLow_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClosLDPhi%sUncLow_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5) ]
                    histClosUp += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)]
                    histClosDw += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5) ]
            hist.SetBinContent(1,multijet)
            #hist.SetBinError(1,multijet*0.25)
            hist.SetBinError(1,multijets_statunc[a-1]) # stat uncertainty
            histUp.SetBinContent(1,multijet*1.387)
            histUp.SetBinError(1,0.0)
            histDw.SetBinContent(1,multijet/1.387)
            histDw.SetBinError(1,0.0)
            isLowDPhiBin=(imult in [0,1,2,3,4]) # separates the low and high dphijj MJ uncertainties
            # setting the default value
            for itr in range(0,len(histClosUp)):
                histClosUp[itr].SetBinContent(1,multijet) 
                histClosUp[itr].SetBinError(1,0.0)
                histClosDw[itr].SetBinContent(1,multijet)
                histClosDw[itr].SetBinError(1,0.0)                    
            if  year==2016:
                if isLowDPhiBin:
                    histClosUp[0].SetBinContent(1,multijet) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                    histClosDw[0].SetBinContent(1,multijet)
                    histClosUp[1].SetBinContent(1,multijet*1.8) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                    histClosDw[1].SetBinContent(1,multijet/1.8)
                else:
                    histClosUp[0].SetBinContent(1,multijet*1.8) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                    histClosDw[0].SetBinContent(1,multijet/1.8)
                    histClosUp[1].SetBinContent(1,multijet) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                    histClosDw[1].SetBinContent(1,multijet)
                histClosUp[2].SetBinContent(1,multijet*1.54) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                histClosDw[2].SetBinContent(1,multijet/1.54)
            if  year==2017:
                histUp.SetBinContent(1,multijet*1.189)
                histDw.SetBinContent(1,multijet/1.189)
                if isLowDPhiBin:
                    histClosUp[3].SetBinContent(1,multijet) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                    histClosDw[3].SetBinContent(1,multijet)
                    histClosUp[4].SetBinContent(1,multijet*1.47) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                    histClosDw[4].SetBinContent(1,multijet/1.47)
                else:
                    histClosUp[3].SetBinContent(1,multijet*1.72) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                    histClosDw[3].SetBinContent(1,multijet/1.72)
                    histClosUp[4].SetBinContent(1,multijet) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                    histClosDw[4].SetBinContent(1,multijet)
                if not doTMVA:
                    histClosUp[5].SetBinContent(1,multijet*1.24) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                    histClosDw[5].SetBinContent(1,multijet/1.24)
                else:
                    histClosUp[5].SetBinContent(1,multijet*1.24) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                    histClosDw[5].SetBinContent(1,multijet/1.24)
            if  year==2018:
                histUp.SetBinContent(1,multijet*1.226)
                histDw.SetBinContent(1,multijet/1.226)
                if isLowDPhiBin:
                    histClosUp[6].SetBinContent(1,multijet) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                    histClosDw[6].SetBinContent(1,multijet)
                    histClosUp[7].SetBinContent(1,multijet*1.62) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                    histClosDw[7].SetBinContent(1,multijet/1.62)
                else:
                    histClosUp[6].SetBinContent(1,multijet*1.32) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                    histClosDw[6].SetBinContent(1,multijet/1.32)
                    histClosUp[7].SetBinContent(1,multijet) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                    histClosDw[7].SetBinContent(1,multijet)
                if not doTMVA:
                    histClosUp[8].SetBinContent(1,multijet*1.19) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                    histClosDw[8].SetBinContent(1,multijet/1.19)
                else:
                    histClosUp[8].SetBinContent(1,multijet*1.19) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                    histClosDw[8].SetBinContent(1,multijet/1.19)
            hist.Write()
            histUp.Write()
            histDw.Write()
            for itr in range(0,len(histClosUp)):
                histClosUp[itr].Write()
                histClosDw[itr].Write()
            a += 1
    else: # write a single histogram
        histClosUp=[]
        histClosDw=[]
        a=89
        b=1
        nbins=len(multijets)*9
        hist   = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        histUp = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncHigh_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        histDw = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJCoreUncLow_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        for yea in [2016, 2017, 2018]:
            histClosUp += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)]
            histClosDw += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5) ]
        for multijet in multijets:
            print multijet
            hist.SetBinContent(a,multijet)
            hist.SetBinError(a,multijets_statunc[b-1]) # stat uncertainty
            histUp.SetBinContent(a,multijet*1.28)
            histUp.SetBinError(a,0.0)
            histDw.SetBinContent(a,multijet/1.28)
            histDw.SetBinError(a,0.0)
            # setting the default value
            for itr in range(0,len(histClosUp)):
                histClosUp[itr].SetBinContent(a,multijet) 
                histClosUp[itr].SetBinError(a,0.0)
                histClosDw[itr].SetBinContent(a,multijet)
                histClosDw[itr].SetBinError(a,0.0)                    
            if  year==2016:
                histClosUp[0].SetBinContent(a,multijet*1.8) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                histClosDw[0].SetBinContent(a,multijet/1.8)
            if  year==2017:
                histUp.SetBinContent(a,multijet*1.25) 
                histDw.SetBinContent(a,multijet/1.25)
                histClosUp[1].SetBinContent(a,multijet*1.5) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                histClosDw[1].SetBinContent(a,multijet/1.5)
            if  year==2018:
                histUp.SetBinContent(a,multijet*1.22)
                histDw.SetBinContent(a,multijet/1.22)
                histClosUp[2].SetBinContent(a,multijet*1.32) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                histClosDw[2].SetBinContent(a,multijet/1.32)

            a+=1
            b+=1
        # writing output
        hist.Write()
        histUp.Write()
        histDw.Write()
        for itr in range(0,len(histClosUp)):
            histClosUp[itr].Write()
            histClosDw[itr].Write()
    #f_multijet.Write()
    f_multijet.Close()

def writeFakeEleGam(Binning=0, year=2016, METCut=150, doTMVA=False, doMTFit=False, isOneCRBin=True):
    f_fakeele = ROOT.TFile("fakeele.root", "recreate")
    #fakeeles = [10.7, 11.6, 7.0, 5.0]
    fakeeles = [7.1, 7.1, 7.1, 7.1]
    if doMTFit:
        fakeeles = [7.1, 7.1, 7.1, 7.1, 7.1]
        if Binning==14:
            fakeeles += [7.1, 7.1, 7.1, 7.1, 7.1]
    a=1
    if isOneCRBin:
        fakeeles=[7.1] # for the inclusive CR

    for fakeelep in fakeeles:
        histSR = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowMT = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowMTLow = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"FakeElUncLow_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"FakeElUncLow_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowMTHigh = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"FakeElUncHigh_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"FakeElUncHigh_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowMT.SetBinContent(1, fakeelep)
        histLowMT.SetBinError(1, fakeelep*0.1)
        histSR.SetBinContent(1, 1.0)
        histSR.SetBinError(1, 0.1)
        histLowMTLow.SetBinContent(1, 1.4)
        histLowMTHigh.SetBinContent(1, 1.0/1.4)

        # write out the histograms
        histLowMT.Write()
        histSR.Write()
        histLowMTLow.Write()
        histLowMTHigh.Write()
        a+=1
    f_fakeele.Close()
    
def writeSinglePhoton(Binning=0, year=2016, METCut=150, doTMVA=False, doMTFit=False):
    f_ph = ROOT.TFile("HFSinglePhoton.root", "recreate")
    ph_tot = 1.42/3.0 # divide because of the 3 periods
    fakephs = [0.52, 0.30, 0.09, 0.07]
    if doTMVA:
        fakephs = [0.5361, 0.4373, 0.0266, 0.0001]
    if doMTFit:
        ph_tot = 37.8/3.0 # divide because of the 3 periods
        fakephs = [0.47, 0.37, 0.13, 0.015, 0.005]
        if Binning==14:
            fakephs = [0.47*0.82, 0.37*0.82, 0.13*0.82, 0.015*0.82, 0.005*0.82]
            fakephs += [0.47*0.18, 0.37*0.18, 0.13*0.18, 0.015*0.18, 0.005*0.18]
    # Compute the totals
    for i in range(0,len(fakephs)):
        fakephs[i]=fakephs[i]*ph_tot
    a=1
    for fakeph in fakephs: #GJetTrig__1up,GJetCore__1up
        histSR = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowTrig = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigLow_SR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histHighTrig = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigHigh_SR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowCore = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreLow_SR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histHighCore = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreHigh_SR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histSR.SetBinContent(1, fakeph)
        histSR.SetBinError(1, 0.25*fakeph)
        histLowTrig.SetBinContent(1, fakeph*1.80)
        histHighTrig.SetBinContent(1, fakeph/1.80)
        histLowCore.SetBinContent(1, fakeph*1.39)
        histHighCore.SetBinContent(1, fakeph/1.39)

        # write out the histograms
        histSR.Write()
        histLowTrig.Write()
        histLowCore.Write()
        histHighTrig.Write()
        histHighCore.Write()
        a+=1
    ### photon for centrality reversed region
    #ph_tot=3.46/3.0
    ph_tot=0.7/3.0
    a=1
    for fakeph in fakephs: #GJetTrig__1up,GJetCore__1up
        histSR = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"Nom_twoLepCR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"Nom_twoLepCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowTrig = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigLow_twoLepCR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigLow_twoLepCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histHighTrig = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigHigh_twoLepCR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetTrigHigh_twoLepCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histLowCore = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreLow_twoLepCR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreLow_twoLepCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histHighCore = ROOT.TH1F("hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreHigh_twoLepCR"+str(a)+"_obs_cuts", "hSinglePhoton_VBFjetSel_"+str(a)+"GJetCoreHigh_twoLepCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histSR.SetBinContent(1, fakeph)
        histSR.SetBinError(1, 0.17*fakeph)
        histLowTrig.SetBinContent(1, fakeph*1.50)
        histHighTrig.SetBinContent(1, fakeph/1.50)
        histLowCore.SetBinContent(1, fakeph*1.39)
        histHighCore.SetBinContent(1, fakeph/1.39)

        # write out the histograms
        histSR.Write()
        histLowTrig.Write()
        histLowCore.Write()
        histHighTrig.Write()
        histHighCore.Write()
        a+=1
    f_ph.Close()
    
def writeFakeEle(Binning=0, year=2016, doDoubleRatio=False, singleHist=False, METCut=150):

    f_fakeele = ROOT.TFile("fakeele.root", "recreate")
    fakeelesp = [10.7, 11.6, 5.0]
    fakeelesm = [10.7, 11.6, 5.0]
    if Binning==1:
        fakeelesp += [9.3]
        fakeelesm += [9.3]
    if Binning==2:
        fakeelesp += [5.3]
        fakeelesm += [5.3]
    if Binning>2 or Binning==-1:
        fakeelesp = [10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
        fakeelesm = [10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
    if Binning==6:
        fakeelesp += [5.3]
        fakeelesm += [5.3]
    if Binning==7:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
    if Binning==8:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
    if Binning==9:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
    if Binning==10:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2, 14.2, 6.2 ,5.3]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2, 14.2, 6.2, 5.3]
    if Binning==11 or Binning==12 or Binning==13 or Binning==21 or Binning==22: # set for all years
        fakeelesp = [8.3, 11.1, 6.7, 4.0, 1.9, 8.3, 11.1, 6.7, 4.0, 1.9, 9.1]
        fakeelesm = [8.3, 11.1, 6.7, 4.0, 1.9, 8.3, 11.1, 6.7, 4.0, 1.9, 9.1] # met>150 numbers
        if METCut==160:
            fakeelesp = [8.4, 11.0, 6.6, 3.9, 4.0, 8.4, 11.0, 6.6, 3.9, 4.0, 7.0]
            fakeelesm = [8.4, 11.0, 6.6, 3.9, 4.0, 8.4, 11.0, 6.6, 3.9, 4.0, 7.0]
        if METCut==200:
            fakeelesp = [4.3, 6.4, 10.6, 5.1, 5.7, 4.3, 6.4, 10.6, 5.1, 5.8, 4.9]
            fakeelesm = [4.3, 6.4, 10.6, 5.1, 5.7, 4.3, 6.4, 10.6, 5.1, 5.8, 4.9]
        if Binning==21 or Binning==22:
            fakeelesp+=[4.9,4.9]
            fakeelesm+=[4.9,4.9]
        if Binning==22:
            fakeelesp+=[6.6, 3.9, 4.0]
            fakeelesm+=[6.6, 3.9, 4.0]
    if Binning==23: # drop the dphijj binning
        fakeelesp = [4.3, 6.4, 10.6, 5.1, 5.7, 4.3, 4.3, 4.3, 6.6, 3.9, 4.0]
        fakeelesm = [4.3, 6.4, 10.6, 5.1, 5.7, 4.3, 4.3, 4.3, 6.6, 3.9, 4.0]
    if (Binning==30 or Binning==40): # drop the dphijj binning
        fakeelesp = [4.3, 6.4, 10.6, 5.1, 5.7]
        fakeelesm = [4.3, 6.4, 10.6, 5.1, 5.7]
    fakeInit = [9.0238,7.4043,3.1402,3.5567,1.5765,8.6259,7.2854,3.5912,5.6147,0.8996,8.44,1.0,1.0,1.0,1.0,1.0,1.0]
    if doDoubleRatio:
        fakeelesp+=[12.5]
        fakeelesm+=[12.5]
    a = 1
    if not singleHist:
        for fakeelep in fakeelesp:
            fakeelem = fakeelesm[a-1]
            histpLowSig=None
            histmLowSig=None
            if doDoubleRatio and a==(len(fakeelesp)):
                histpLowSig = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneElePosLowSigCR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneElePosLowSigCR1_obs_cuts;;", 1, 0.5, 1.5)
                histmLowSig = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneEleNegLowSigCR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneEleNegLowSigCR1_obs_cuts;;", 1, 0.5, 1.5)
                histLowSig = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneEleLowSigCR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneEleLowSigCR1_obs_cuts;;", 1, 0.5, 1.5)                
            else:
                histpLowSig = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histmLowSig = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histLowSig = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)                
            histpLowSig.SetBinContent(1,fakeInit[a-1]/3.0*fakeelep)
            histmLowSig.SetBinContent(1,fakeInit[a-1]/3.0*fakeelem)
            histLowSig.SetBinContent(1,fakeInit[a-1]/3.0*fakeelem)
            histpLowSig.Write()
            histmLowSig.Write()
            histLowSig.Write()
            histm=None
            histp=None
            histe=None
            histpUncUpLowMjj=None
            histpUncDwLowMjj=None
            histpUncUpHighMjj=None
            histpUncDwHighMjj=None
            histeUncUpLowMjj=None
            histeUncDwLowMjj=None
            histeUncUpHighMjj=None
            histeUncDwHighMjj=None            
            histmUncUpLowMjj=None
            histmUncDwLowMjj=None
            histmUncUpHighMjj=None
            histmUncDwHighMjj=None

            if doDoubleRatio and a==(len(fakeelesp)):
                histp = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneElePosACR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneElePosACR1_obs_cuts;;", 1, 0.5, 1.5)
                histm = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneEleNegACR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneEleNegACR1_obs_cuts;;", 1, 0.5, 1.5)
            else:
                histp = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histe = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)                
                histm = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histpUncUpLowMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncHigh_oneElePosCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncHigh_oneElePosCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histpUncDwLowMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncLow_oneElePosCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncLow_oneElePosCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histpUncUpHighMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncHigh_oneElePosCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncHigh_oneElePosCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histpUncDwHighMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncLow_oneElePosCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncLow_oneElePosCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histeUncUpLowMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncHigh_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncHigh_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histeUncDwLowMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncLow_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"LPTFakeElUncLow_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histeUncUpHighMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncHigh_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncHigh_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histeUncDwHighMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncLow_oneEleCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"HPTFakeElUncLow_oneEleCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)                
                histmUncUpLowMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"LPTFakeElmUncHigh_oneEleNegCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"LPTFakeElmUncHigh_oneEleNegCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histmUncDwLowMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"LPTFakeElmUncLow_oneEleNegCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"LPTFakeElmUncLow_oneEleNegCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histmUncUpHighMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"HPTFakeElmUncHigh_oneEleNegCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"HPTFakeElmUncHigh_oneEleNegCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histmUncDwHighMjj = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"HPTFakeElmUncLow_oneEleNegCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"HPTFakeElmUncLow_oneEleNegCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histp.SetBinContent(1,fakeInit[a-1]/3.0)
            histm.SetBinContent(1,fakeInit[a-1]/3.0)
            histe.SetBinContent(1,fakeInit[a-1]/3.0)            
            
            if (a>=1 and a<=3) or (a>=6 and a<=8) or a==11:
                histpUncUpLowMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.2)
                histpUncDwLowMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.2)
                histmUncUpLowMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.2)
                histmUncDwLowMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.2)
                histpUncUpHighMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.1)
                histpUncDwHighMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.1)
                histmUncUpHighMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.1)
                histmUncDwHighMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.1)
                histeUncUpHighMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.1)
                histeUncDwHighMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.1)
                histeUncUpLowMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.2)
                histeUncDwLowMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.2)
            else:
                histpUncUpLowMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.1)
                histpUncDwLowMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.1)
                histmUncUpLowMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.1)
                histmUncDwLowMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.5)
                histpUncUpHighMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.5)
                histpUncDwHighMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.5)
                histmUncUpHighMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.5)
                histmUncDwHighMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.5)
                histeUncUpLowMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.1)
                histeUncDwLowMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.1)
                histeUncUpHighMjj.SetBinContent(1,fakeInit[a-1]/3.0*1.5)
                histeUncDwHighMjj.SetBinContent(1,fakeInit[a-1]/3.0/1.5)
                
            histp.Write()
            histm.Write()
            histe.Write()
            histpUncUpLowMjj.Write()
            histpUncDwLowMjj.Write()
            histpUncUpHighMjj.Write()
            histpUncDwHighMjj.Write()
            histeUncUpLowMjj.Write()
            histeUncDwLowMjj.Write()
            histeUncUpHighMjj.Write()
            histeUncDwHighMjj.Write()            
            histmUncUpLowMjj.Write()
            histmUncDwLowMjj.Write()
            histmUncUpHighMjj.Write()
            histmUncDwHighMjj.Write()
            a += 1
    else: # write out a single histogram
        nbins=len(fakeelesp)*9
        binshift=len(fakeelesp)
        a=1
        histp = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        histm = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5) 

        for fakeelep in fakeelesp:
            fakeelem = fakeelesm[a-1]
            histp.SetBinContent(a+binshift*3,1)
            histm.SetBinContent(a+binshift*2,1)
            a += 1
        histp.Write()
        histm.Write()
    #f_fakeele.Write()
    f_fakeele.Close()

def writeFakeMuo(Binning=0, year=2016, METCut=150):
    f_fakemuo = ROOT.TFile("fakemuo.root", "recreate")
    fakemuos=[]
    fakemuos = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.0, 3.0, 3.0, 3.0]
    if Binning==11 or Binning==12 or Binning==13 or Binning==21 or Binning==22: # set for all years
        fakemuos = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.0, 3.0, 3.0, 3.0]
        if METCut==160:
            fakemuos = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.0, 3.0, 3.0, 3.0]
        if Binning==21 or Binning==22:
            fakemuos+=[3.0,3.0]
        if Binning==22:
            fakemuos+=[3.0,3.0,3.0]
    if Binning==23:
        fakemuos = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.0, 3.0, 3.0, 3.0]
    if (Binning==30 or Binning==40):
        fakemuos = [3.0, 3.0, 3.0, 3.0, 3.0]
            
    a=1
    hists=[]
    histcr=None
    hist=None
    for fakemuo in fakemuos:
        histcr = ROOT.TH1F("hmuoFakes_VBFjetSel_"+str(a)+"Nom_oneMuMTCR"+str(a)+"_obs_cuts", "hmuoFakes_VBFjetSel_"+str(a)+"Nom_oneMuMTCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        hist = ROOT.TH1F("hmuoFakes_VBFjetSel_"+str(a)+"Nom_oneMuCR"+str(a)+"_obs_cuts", "hmuoFakes_VBFjetSel_"+str(a)+"Nom_oneMuCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histcr.SetBinContent(1,fakemuo)
        histcr.SetBinError(1,fakemuo*0.3)
        hist.SetBinContent(1,1.0)
        hist.SetBinError(1,0.2)
        hists+=[histcr,hist]
        a += 1
    f_fakemuo.cd()
    for h in hists:
        h.Write()
    f_fakemuo.Close()
#writeMultiJetFJVT(11, 2016, 150)
#writeMultiJet(11, 2016, 150)
#writeMultiJet(11, 2018, 160)
#os.chdir('../v34D')
#writeMultiJet(11, 2017, 150)
#os.chdir('../v34E')
#writeMultiJet(11, 2018, 150)
#writeFakeEle(11,  2018, METCut=200)
#writeFakeMuo(11)

import ROOT
import sys,os
import math
from optparse import OptionParser
#
# python ../VBFAnalysis/scripts/sysPlotv2.py --binNum 4 --ph-ana --ZeroCheck --combinePlusMinus --oneCRBin -i /tmp/HFALLGamMVAv2Syst.New.root --syst JET_Flavor_Response --inputUpdate /tmp/HFALLGamMVAv2Syst.update.root --saveAs pdf
#
def HistName(histName, regionName, systName, binNum):
    return "h"+histName+"_"+(regionName.replace('X','%s' %binNum)).replace('Nom_',systName+'_')

#-----------------------------------------
def BinomialErr(n2, n1, err1=0.0):
    err=0.0
    if n1==0:
        return err
    total_num=n1
    if err1>0.0:
        total_num = (n1/err1)**2

    eff = n2/n1
    if eff>1.0 or eff<0.0:
        print 'eff too high',eff
        return 0
    err = math.sqrt(eff*(1.0-eff)/total_num)
    return err

def SetBinomialErrorRatio(hsys,hnom):
    for ib in range(1,hnom.GetNbinsX()+1):
        ratio = 1.0
        nomV=hnom.GetBinContent(ib)
        sysV=hsys.GetBinContent(ib)
        if nomV>0.0:
            ratio=sysV/nomV
        hsys.SetBinContent(ib,ratio)
        if nomV>sysV and nomV>0.0: 
            hsys.SetBinError(ib,BinomialErr(sysV,nomV,hnom.GetBinError(ib)))
        elif sysV>0.0:
            hsys.SetBinError(ib,BinomialErr(nomV,sysV,hnom.GetBinError(ib)))
        else:
            hsys.SetBinError(ib,0.0)                        
        

def DeclareCanvas(options):

    can=ROOT.TCanvas("c1","c1",1600,1000)
    if options.ratio:
        can.Divide(1,2)
        can.cd(1)
        ROOT.gPad.SetBottomMargin(0)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0.3,1,1)
        can.cd(2)
        ROOT.gPad.SetTopMargin(0)
        ROOT.gPad.SetBottomMargin(0.35)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0,1,0.3)
        can.cd(1)
    return can

def DrawRatio(options,can,nom, varHist=[]):
    color=1
    drawOpt=''
    for v in varHist:
        v.Divide(nom)
        v.GetYaxis().SetRangeUser(0.9,1.1)
        v.SetLineColor(color)
        color+=1
        v.Draw(drawOpt)
        drawOpt='same'

    can.Update()
    can.WaitPrimitive()

def PhotonError():
    rNewfile=ROOT.TFile(options.inputUpdate,'UPDATE')
    keysF = rNewfile.GetListOfKeys()
    updateList=[]
    for i in range(1,11):
        hnomName = 'hSinglePhoton_VBFjetSel_%sNom_SR%s_obs_cuts' %(i,i)
        hupName = 'hSinglePhoton_VBFjetSel_%sGJetTrigHigh_SR%s_obs_cuts' %(i,i)
        hdwName = 'hSinglePhoton_VBFjetSel_%sGJetTrigLow_SR%s_obs_cuts' %(i,i)

        hnom=rNewfile.Get(hnomName)
        hup=rNewfile.Get(hupName)
        hdw=rNewfile.Get(hdwName)
        hup.SetBinContent(1,hnom.GetBinContent(1)*2.0)
        hdw.SetBinContent(1,hnom.GetBinContent(1)/2.0)
        updateList+=[hup, hdw]

    # write the updated histograms
    for ha in updateList:
        rNewfile.cd()
        ha.Write(ha.GetName(),ROOT.TObject.kOverwrite)
        print ha.GetName(),' set value photon jet: ',ha.Integral()
    rNewfile.Close()

def MGCentralValue(regions):
    rNewfile=ROOT.TFile(options.inputUpdate,'UPDATE')
    keysF = rNewfile.GetListOfKeys()
    updateList=[]
    sfactorMap={1:1.07,2:0.98, 3:0.85, 4:0.62}
    #sfactorMap={1:1.035,2:0.99, 3:0.925, 4:0.81}
    #sfactorMap={1:0.98,2:1.02, 3:1.03, 4:1.05} # for keras
    #sfactorErrMap={1:1.07,2:0.98, 3:0.85, 4:0.62}

    sfactorMapSRW={1:1.08,2:1.05, 3:0.78, 4:0.83}
    sfactorMapZCR={1:1.02,2:1.10, 3:1.1, 4:0.88}

    doErrorOnly=False # when true this does not change the central value
    doCorrWZMG=False
    for reg in regions:
        sfactorMap=sfactorMapSRW
        if reg.count('_two'):
            sfactorMap=sfactorMapZCR            
        for sam in ['Zg_strong','Wg_strong']:
            for i in range(1,5):
                if i not in sfactorMap:
                    print 'will crash. define the new bins'
                sfactor=sfactorMap[i]
                hnomName = 'h%s_VBFjetSel_%sNom_SR%s_obs_cuts' %(sam, i,i)
                hupName  = 'h%s_VBFjetSel_%sMGCompareHigh_SR%s_obs_cuts' %(sam, i,i)
                hdwName  = 'h%s_VBFjetSel_%sMGCompareLow_SR%s_obs_cuts' %(sam, i,i)
                hnomName = 'h%s_' %(sam) + reg.replace('X','%s' %i) #'VBFjetSel_%sNom_SR%s_obs_cuts' %(sam, i,i)
                hupName = 'h%s_' %(sam) + (reg.replace('X','%s' %i)).replace('Nom_','MGCompareHigh_') #'VBFjetSel_%sNom_SR%s_obs_cuts' %(sam, i,i)
                hdwName = 'h%s_' %(sam) + (reg.replace('X','%s' %i)).replace('Nom_','MGCompareLow_') #'VBFjetSel_%sNom_SR%s_obs_cuts' %(sam, i,i)
                if sam=="Wg_strong" and not doCorrWZMG:
                    hupName = 'h%s_' %(sam) + (reg.replace('X','%s' %i)).replace('Nom_','MGCompareWHigh_') #'VBFjetSel_%sNom_SR%s_obs_cuts' %(sam, i,i)
                    hdwName = 'h%s_' %(sam) + (reg.replace('X','%s' %i)).replace('Nom_','MGCompareWLow_') #'VBFjetSel_%sNom_SR%s_obs_cuts' %(sam, i,i)
                print hnomName
                print hupName
                print hdwName
                hnom=rNewfile.Get(hnomName)
                hup = hnom.Clone()
                hdw = hnom.Clone()
                hup.SetTitle(hupName)
                hup.SetName(hupName)
                hdw.SetTitle(hdwName)
                hdw.SetName(hdwName)
                hdw.Scale(sfactor)
                if doErrorOnly:
                    hup.SetBinContent(1,hup.GetBinContent(1) + (hup.GetBinContent(1)-hdw.GetBinContent(1)))
                else:
                    hdw.SetBinContent(1,hdw.GetBinContent(1) - (hup.GetBinContent(1)-hdw.GetBinContent(1)))
                hup.SetDirectory(rNewfile)
                hup.Write()
                updateList+=[hup]
                hdw.SetDirectory(rNewfile)
                hdw.Write()
                updateList+=[hdw]

    for k in keysF:
        kname=k.GetName()
        if kname.count('MGCompare'):
            continue
        if kname.count('Zg_strong') or kname.count('Wg_strong'):
            h=rNewfile.Get(kname)
            sfactor=1.0
            if kname.count('VBFjetSel_1'):
                sfactor=sfactorMap[1]
            elif kname.count('VBFjetSel_2'):
                sfactor=sfactorMap[2]
            elif kname.count('VBFjetSel_3'):
                sfactor=sfactorMap[3]
            elif kname.count('VBFjetSel_4'):
                sfactor=sfactorMap[4]
                #sfactor=0.85
            if not doErrorOnly:
                h.Scale(sfactor)
                updateList+=[h]
                    
    # write the updated histograms
    for ha in updateList:
        rNewfile.cd()
        ha.Write(ha.GetName(),ROOT.TObject.kOverwrite)
        print ha.GetName(),' adding and saving this histogram for MGCentralValue'
    rNewfile.Close()   

def applyEWKNLO():

    rNewfile=ROOT.TFile(options.inputUpdate,'UPDATE')
    keysF = rNewfile.GetListOfKeys()
    updateList=[]
    for k in keysF:
        kname=k.GetName()
        if kname.count('Zg_strong') or kname.count('Wg_strong'):
            h=rNewfile.Get(kname)
            sfactor=1.0
            if kname.count('VBFjetSel_1'):
                sfactor=0.985
            elif kname.count('VBFjetSel_2'):
                sfactor=0.959
            elif kname.count('VBFjetSel_3'):
                sfactor=0.970
            elif kname.count('VBFjetSel_4'):
                sfactor=0.958
            h.Scale(sfactor)
            updateList+=[h]
                    
    # write the updated histograms
    for ha in updateList:
        rNewfile.cd()
        ha.Write(ha.GetName(),ROOT.TObject.kOverwrite)
        print ha.GetName(),' set value to 0'
    rNewfile.Close()
def ZeroCheck():

    rNewfile=ROOT.TFile(options.inputUpdate,'UPDATE')
    keysF = rNewfile.GetListOfKeys()
    updateList=[]

    for k in keysF:
        kname=k.GetName()
        if '_AFII' in kname and 'dark125' in kname:
            print 'AFII',kname
            krep = kname.replace('JET_RelativeNonClosure_AFIIHigh','Nom')
            for y in ['JET_PunchThrough_AFIIHigh','JET_PunchThrough_AFIILow','JET_RelativeNonClosure_AFIIHigh','JET_RelativeNonClosure_AFIILow','JET_JER_DataVsMC_AFIIHigh','JET_JER_DataVsMC_AFIILow']:
                krep = krep.replace(y,'Nom')
            h=rNewfile.Get(kname)
            print krep
            hnom=rNewfile.Get(krep)
            h.SetBinContent(1,hnom.GetBinContent(1))
            updateList+=[h]
        listOfAF2ToRm = ['JET_PunchThrough_MC16High','JET_PunchThrough_MC16Low','JET_JER_DataVsMC_MC16Low','JET_JER_DataVsMC_MC16High']
        listOfAF2ToRmBool=False
        for y in listOfAF2ToRm:
            if y in kname:
                listOfAF2ToRmBool=True
                break
        if listOfAF2ToRmBool and 'dark' in kname and ('125' not in kname):
            print 'JER AFII test: ',kname
            krep = kname.replace('JET_PunchThrough_MC16High','Nom')
            for y in listOfAF2ToRm:
                krep = krep.replace(y,'Nom')
            h=rNewfile.Get(kname)
            print krep
            hnom=rNewfile.Get(krep)
            h.SetBinContent(1,hnom.GetBinContent(1))
            updateList+=[h]
        if (kname.count("Z_strong") and kname.count('_one')) or (kname.count("ttbar") and kname.count('_one')) or (kname.count("W_strong") and kname.count('_two')) or (kname.count("Zg_strong") and kname.count('_one')) or (kname.count("Wg_strong") and kname.count('_two')) or  (kname.count("Wg_EWK") and kname.count('_two')) or (kname.count("Zg_EWK") and kname.count('_one')) or options.ph_ana or kname.count('FJVTCR'):
            h=rNewfile.Get(kname)
            if h.GetBinContent(1)<0.0:
                h.SetBinContent(1,0.0)
                updateList+=[h]
    # write the updated histograms
    for ha in updateList:
        rNewfile.cd()
        ha.Write(ha.GetName(),ROOT.TObject.kOverwrite)
        print ha.GetName(),' set value to 0'
    rNewfile.Close()
    
def GetLegLabel(options,can):

    #ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9)
    ROOT.gPad.SetTickx(True);
    ROOT.gPad.SetTicky(True);
    texts = ATLAS.getATLASLabels(can, 0.4, 0.78, options.lumi, selkey="")
    for text in texts:
        text.Draw()

def PrintPulls(rfile,options,can,histName,regions):
    print 'Reading file: ',options.pullsFile
    if not os.path.exists(options.pullsFile):
        print 'file does not exist'
    pullMap={}
    pullList = open(options.pullsFile)
    systFile=open('../listTheorySyst11STv4')
    systMap={}
    key=''
    for l in systFile:
        if l.count('SRup'):
            key='SRup'
            continue
        elif l.count('SRdown'):
            key='SRdown'
            continue
        elif l.count('ZCRdown'):
            key='ZCRdown'
            continue
        elif l.count('ZCRup'):
            key='ZCRup'
            continue
        elif l.count('WCRdown'):
            key='WCRdown'
            continue        
        elif l.count('WCRup'):
            key='WCRup'
            continue
        if not l.strip():
            continue
        sLine=l.strip().split(' ')
        if key not in systMap:
            systMap[key]={}
        #print sLine[0],sLine[1]
        systMap[key][sLine[0]+"_bin1"]=sLine[1].rstrip('\n').split(',')
        
    for i in pullList:
        myList= i.strip().rstrip('\n').split(' ')
        myList=filter(None, myList)
        #print myList
        if myList[0].count('alpha_'):
            pullMap[myList[0].replace('alpha_','')]=[float(myList[2]),float(myList[4])]
    for r in regions:
        rkey='SR'
        if r.count('two'):
            rkey='ZCR'
        if r.count('one'):
            rkey='WCR'
        #for ibin in range(1,options.binNum+1):
        totalValPull=0.0
        for ibin in [4,9,5,10]:
            
            nomBinH=rfile.Get(HistName(histName, r, 'Nom', ibin))
            nomVal=nomBinH.GetBinContent(1)
            print 'Bin: ',ibin,nomBinH.GetBinContent(1)
            if not nomBinH:
                print 'could not load Nominal: ',HistName(histName, r, 'Nom', ibin)
                continue
            totalValPull=nomBinH.GetBinContent(1)
            for systName,pulls in pullMap.iteritems():
                pullValue = pulls[0]/pulls[1]
                #print pullValue
                sysBinH=rfile.Get(HistName(histName, r, systName+'High', ibin))
                #print systName #,systMap[rkey+'up']
                #print systName+'_bin1'
                if (systName) in systMap[rkey+'up']:
                    #print 'FOUND:',systName
                    if not systName.count(histName):
                        continue
                    upPull=pullValue*(nomVal)*(float(systMap[rkey+'up'][systName][ibin-1])-1.0)
                    dwPull=pullValue*(nomVal)*(float(systMap[rkey+'down'][systName][ibin-1])-1.0)                    
                    if abs(dwPull)>0.01 or  abs(upPull)>0.01:
                        print '%0.2f %0.2f %s %s THEORY %s bin %s' %(upPull, dwPull, systName,histName, r,ibin)
                upPull=0.0
                dwPull=0.0
                if sysBinH:
                    upPull=pullValue*(nomVal-sysBinH.GetBinContent(1))
                    #print 'could not load Syst: ',HistName(histName, r, systName+'High', ibin)
                    #continue
                sysBinL=rfile.Get(HistName(histName, r, systName+'Low', ibin))
                if sysBinL:
                    dwPull=pullValue*(nomVal-sysBinL.GetBinContent(1))
                    #print 'could not load Syst: ',HistName(histName, r, systName+'Low', ibin)
                    #continue
                
                #print 'pull values:',upPull,dwPull
                if abs(dwPull)>0.01 or  abs(upPull)>0.01:
                    if pullValue>0.0:
                        print '%0.2f + %0.2f %s %s' %(nomVal,upPull,systName,histName)
                        totalValPull+=upPull
                    else:
                        print '%0.2f - %0.2f %s %s' %(nomVal,dwPull,systName,histName)
                        totalValPull-=dwPull
            print 'totalValPull: %0.2f' %totalValPull,' bin ',ibin
    pullList.close()

#symmeterize systematics
def Symmeterize(hnom, hup, hdw):

    for i in range(1,hnom.GetNbinsX()+1):
        inom=hnom.GetBinContent(i)
        iup =hup.GetBinContent(i)
        idw =hdw.GetBinContent(i)
        if iup!=0.0:
            hdw.SetBinContent(i,inom/iup*inom)
    
def Smooth(rfile,options,can,systName,histName,regions,systNameToSymmet):
    inputMap={'alphaS':   0.018,
              'EV30':   -0.046,
              'EV29':   -0.006,
              'EV28':   -0.042,
              'EV27':   -0.011,
              'EV26':   -0.008,
              'EV25':   -0.036,
              'EV24':    0.021,
              'EV23':   -0.034,
              'EV22':   -0.031,
              'EV21':   -0.056,
              'EV20':   -0.047,
              'EV19':   -0.023,
              'EV18':   -0.072,
              'EV17':   -0.001,
              'EV16':   -0.011,
              'EV15':   -0.028,
              'EV14':    0.037,
              'EV13':   -0.017,
              'EV12':    0.018,
              'EV11':   -0.033,
              'EV10':   -0.029,
              'EV9':   -0.033,
              'EV8':    0.026,
              'EV7':   -0.048,
              'EV6':    0.043,
              'EV5':   -0.010,
              'EV4':   -0.022,
              'EV3':    0.027,
              'EV2':   -0.022,
              'EV1':   -0.038}
    smoothSyle=1
    if systName.count('EL_'):
        smoothSyle=1
    elif systName.count('JET_'):
        smoothSyle=3
    elif systName.count('MET_'):
        smoothSyle=3
    elif systName.count('PRW_'):
        smoothSyle=3
    if options.ph_ana and histName.count('ttbar'):
        smoothSyle=1
    nomMap={}
    sysUpMap={}
    sysDwMap={}
    binOrder=[1,3,5,7,9,2,4,6,8,10,11,12,13,14,15,16]
    if options.ph_ana:
        binOrder = [1,2,3,4,5,6,7,8,9,10]

    for r in regions:
        binNum = options.binNum
        if options.oneCRBin and not r.count('SR'):
            binNum=1
        hName  =HistName(histName, r, 'Nom', +1)
        hNameUp=HistName(histName, r, 'Up', binNum+1)        
        hNameDw=HistName(histName, r, 'Dw', binNum+1)        
        hSaveName=hName.replace('12Nom_oneEleNegLowSigCR12_obs_cuts','')
        hSaveName=hName.replace('12Nom_oneMuNegCR12_obs_cuts','')
        h=ROOT.TH1F(hName,hName,binNum,0.5,0.5+binNum)
        hsys=ROOT.TH1F(hNameUp,hNameUp,binNum,0.5,0.5+binNum)        
        hsysdw=ROOT.TH1F(hNameDw,hNameDw,binNum,0.5,0.5+binNum)        
        for ibin in range(1,binNum+1):
            nomBinH=rfile.Get(HistName(histName, r, 'Nom', ibin))
            if not nomBinH:
                print 'could not load Nominal: ',HistName(histName, r, 'Nom', ibin)
                continue
            h.SetBinContent(binOrder[ibin-1], nomBinH.GetBinContent(1))
            h.SetBinError  (binOrder[ibin-1], 0.001*nomBinH.GetBinError  (1))
            sysBinH=rfile.Get(HistName(histName, r, systName+'High', ibin))
            if not sysBinH:
                print 'could not load up variation: ',HistName(histName, r, systName+'High', ibin)
            else:
                hsys.SetBinContent(binOrder[ibin-1], sysBinH.GetBinContent(1))
                hsys.SetBinError  (binOrder[ibin-1], 0.0)
            # down variation
            sysdwBinH=rfile.Get(HistName(histName, r, systName+'Low', ibin))
            if not sysdwBinH:
                print 'could not load down variation: ',HistName(histName, r, systName+'Low', ibin)
            else:
                hsysdw.SetBinContent(binOrder[ibin-1], sysdwBinH.GetBinContent(1))
                hsysdw.SetBinError  (binOrder[ibin-1], 0.0)            
        nomMap[r]=h.Clone()
        sysUpMap[r]=hsys.Clone()
        sysDwMap[r]=hsysdw.Clone()

    # takes the integral in the region. Then scales by the integral over all regions
    updateHist=[]
    rNewfile=ROOT.TFile(options.inputUpdate,'UPDATE')
    if options.smooth==1 or (options.smooth==5 and smoothSyle==1):
        print 'smoothing option 1'
        for r in regions:
            binNum = options.binNum
            if options.oneCRBin and not r.count('SR'):
                binNum=1
            nomInt = nomMap[r].Integral(1,binNum)
            upInt  = sysUpMap[r].Integral(1,binNum)
            dwInt  = sysDwMap[r].Integral(1,binNum)
            for ibin in range(1,binNum+1):
                currentNomV=nomMap[r].GetBinContent(binOrder[ibin-1])
                if upInt!=0.0 and nomInt!=0.0:
                    sysBinH=rNewfile.Get(HistName(histName, r, systName+'High', ibin))
                    if not sysBinH:
                        continue
                    #sysBinH.Scale(upInt/nomInt)
                    sysbef=sysBinH.GetBinContent(1)
                    sysBinH.SetBinContent(1,upInt/nomInt*currentNomV)
                    #print 'after: ',nomInt,upInt,currentNomV,sysBinH.GetBinContent(1),sysbef
                    updateHist+=[sysBinH]
                if dwInt!=0.0 and nomInt!=0.0:
                    sysBinH=rNewfile.Get(HistName(histName, r, systName+'Low', ibin))
                    if not sysBinH:
                        continue
                    #sysBinH.Scale(upInt/nomInt)
                    scaleSyst=dwInt/nomInt
                    if systName in systNameToSymmet:
                        if upInt>0.0:
                            scaleSyst=nomInt/upInt
                    sysBinH.SetBinContent(1,scaleSyst*currentNomV)
                    updateHist+=[sysBinH]
    elif options.smooth==2 or (options.smooth==5 and smoothSyle==2):
        print 'smoothing option 2 - parabolic smoothing'
        smooth_tool=ROOT.SmoothHist()
        smooth_tool.setNmax(1)
        # first add the regions
        CombineSysNomMap={}
        CombineSysUpMap={}
        CombineSysDwMap={}
        for r in regions:
            binNum = options.binNum
            if options.oneCRBin and not r.count('SR'):
                binNum=1

            CombineSysNomMap[r]= nomMap[r].Clone()
            CombineSysUpMap[r] = sysUpMap[r].Clone()
            CombineSysDwMap[r] = sysDwMap[r].Clone()
            for r2 in regions:
                if r==r2:
                    continue
                if r.count('two') and r2.count('two'):
                    CombineSysNomMap[r].Add( nomMap[r2])
                    CombineSysUpMap[r]. Add( sysUpMap[r2])
                    CombineSysDwMap[r]. Add( sysDwMap[r2])
                if r.count('one') and r2.count('one'):
                    CombineSysNomMap[r].Add( nomMap[r2])
                    CombineSysUpMap[r]. Add( sysUpMap[r2])
                    CombineSysDwMap[r]. Add( sysDwMap[r2])
            
            sysBefore=sysUpMap[r].Clone()
            hSmoothed = smooth_tool.smoothHistogram(nomMap[r], sysUpMap[r], True)
            smooth_tool.smoothHistogram(nomMap[r], sysDwMap[r], True)            
            if systName in systNameToSymmet:
                Symmeterize(CombineSysNomMap[r],sysUpMap[r],sysDwMap[r])
            if options.wait:
                rhSmoothed = hSmoothed.Clone()                
                DrawRatio(options,can,nomMap[r], varHist=[sysBefore,rhSmoothed])
            for ibin in range(1,binNum+1):
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'High', ibin))
                if not sysBinH:
                    continue
                sysBinH.SetBinContent(1,sysUpMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH]
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'Low', ibin))
                if not sysBinH:
                    continue
                sysBinH.SetBinContent(1,sysDwMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH]
    elif options.smooth==3 or (options.smooth==5 and smoothSyle==3):
        print 'smoothing option 3 - combine regions'
        smooth_tool=ROOT.SmoothHist()
        smooth_tool.setNmax(1)
        
        # first add the regions
        CombineSysNomMap={}
        CombineSysUpMap={}
        CombineSysDwMap={}
        for r in regions:
            CombineSysNomMap[r]= nomMap[r].Clone()
            CombineSysUpMap[r] = sysUpMap[r].Clone()
            CombineSysDwMap[r] = sysDwMap[r].Clone()            
            for r2 in regions:
                if r==r2:
                    continue
                if r.count('two') and r2.count('two'):
                    CombineSysNomMap[r].Add( nomMap[r2])
                    CombineSysUpMap[r]. Add( sysUpMap[r2])
                    CombineSysDwMap[r]. Add( sysDwMap[r2])
                if r.count('one') and r2.count('one'):
                    CombineSysNomMap[r].Add( nomMap[r2])
                    CombineSysUpMap[r]. Add( sysUpMap[r2])
                    CombineSysDwMap[r]. Add( sysDwMap[r2])
                    
        # smooth with the added regions
        for r in regions:
            binNum = options.binNum
            if options.oneCRBin and not r.count('SR'):
                binNum=1
            sysBefore=sysUpMap[r].Clone()
            hSmoothed = smooth_tool.smoothHistogram(CombineSysNomMap[r], CombineSysUpMap[r], True)
            smooth_tool.smoothHistogram(CombineSysNomMap[r], CombineSysDwMap[r], True)
            # symmeterize
            if systName in systNameToSymmet:
                Symmeterize(CombineSysNomMap[r],CombineSysUpMap[r],CombineSysDwMap[r])
            # add flat syst for Z in the the W CR and make sure the systematics don't go in the same direction
            if (histName.count('Z_') and r.count('one')) or (histName.count('W_') and r.count('two')):
                flatNomInt=CombineSysNomMap[r].Integral(1,binNum)
                flatUpInt=CombineSysUpMap[r].Integral(1,binNum)
                flatDwInt=CombineSysDwMap[r].Integral(1,binNum)
                for i in range(1,binNum+1):
                    if flatNomInt>0.0:
                        fracUp=(flatUpInt/flatNomInt)
                        fracDw=(flatDwInt/flatNomInt)
                        if abs(1.-fracUp)>0.08 and fracUp<1.0:
                            fracUp=0.92
                        if abs(1.-fracUp)>0.08 and fracUp>1.0:
                            fracUp=1.08
                        if ((1.-fracUp)<1.0 and  (1.-fracDw)<1.0) or ((1.-fracUp)>1.0 and  (1.-fracDw)>1.0):
                            fracDw=2.-fracUp
                        CombineSysUpMap[r].SetBinContent(i,(flatUpInt/flatNomInt)*CombineSysNomMap[r].GetBinContent(i))
                        CombineSysDwMap[r].SetBinContent(i,(flatDwInt/flatNomInt)*CombineSysNomMap[r].GetBinContent(i))
            if options.wait:
                rhSmoothed = hSmoothed.Clone()                
                DrawRatio(options,can,nomMap[r], varHist=[sysBefore,rhSmoothed])
            for ibin in range(1,binNum+1):
                nomBinH=rNewfile.Get(HistName(histName, r, 'Nom', ibin))
                nomV=nomBinH.GetBinContent(1)
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'High', ibin))
                if not sysBinH:
                    continue
                if nomV!=0.0:
                    sysBinH.SetBinContent(1,nomV*CombineSysUpMap[r].GetBinContent(binOrder[ibin-1])/CombineSysNomMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH]
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'Low', ibin))
                if not sysBinH:
                    continue
                if nomV!=0.0:
                    #print nomV,(nomV*CombineSysDwMap[r].GetBinContent(binOrder[ibin-1])/CombineSysNomMap[r].GetBinContent(binOrder[ibin-1]))
                    sysBinH.SetBinContent(1,nomV*CombineSysDwMap[r].GetBinContent(binOrder[ibin-1])/CombineSysNomMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH]
    elif options.smooth==10:
        print 'smoothing option 10...symmeterize'
        # looked up the max variation for the systematics pre smoothing. the parabolic smoothing can inflate the systematics. reduced this to the max
        maxvariation=-1.0
        minvariation=-1.0
        if systName=='JET_Flavor_Composition': maxvariation=0.04
        if systName=='JET_JER_EffectiveNP_7restTerm': maxvariation=0.03
        if systName=='JET_JER_EffectiveNP_7': maxvariation=0.067; minvariation=0.019
        if systName=='JET_JER_EffectiveNP_3': maxvariation=0.081; minvariation=0.025
        if systName=='JET_JER_EffectiveNP_2': maxvariation=0.091; minvariation=0.02
        if systName=='JET_JER_EffectiveNP_4': maxvariation=0.071; minvariation=0.009
        if systName=='JET_JER_EffectiveNP_5': maxvariation=0.065; minvariation=0.015
        if systName=='JET_JER_EffectiveNP_6': maxvariation=0.091; minvariation=0.029
        if systName=='JET_JER_EffectiveNP_1': maxvariation=0.081; minvariation=0.009
        if systName=='JET_JER_EffectiveNP_11': maxvariation=0.071; minvariation=0.026
        if systName=='JET_JER_EffectiveNP_10': maxvariation=0.065; minvariation=0.021
        if systName=='JET_JER_EffectiveNP_8': maxvariation=0.066; minvariation=0.009
        if systName=='JET_JER_EffectiveNP_12restTerm': maxvariation=0.082; minvariation=0.029
        if systName=='EG_RESOLUTION_ALL': maxvariation=0.04
        if systName=='MET_SoftTrk_ResoPara': maxvariation=0.05
        if systName=='JET_JER_DataVsMC_MC16': maxvariation=0.05
        if systName=='JET_EffectiveNP_Modelling1': maxvariation=0.09
        if systName=='JET_EffectiveNP_Modelling2': maxvariation=0.09
        if systName=='JET_EffectiveNP_Modelling3': maxvariation=0.09
        if systName=='JET_Pileup_RhoTopology': maxvariation=0.05
        if systName=='JET_Flavor_Response': maxvariation=0.04
        if systName=='JET_Pileup_OffsetNPV': maxvariation=0.05
        if systName=='JET_Pileup_PtTerm': maxvariation=0.035
        if systName=='JET_EtaIntercalibration_Modelling': maxvariation=0.04
        if systName=='JET_EtaIntercalibration_TotalStat': maxvariation=0.04
        if systName=='PRW_DATASF': maxvariation=0.025
        if systName=='PH_EFF_ISO_Uncertainty': maxvariation=0.04
        if systName=='MET_SoftTrk_ResoPerp': maxvariation=0.05
        if systName=='MET_SoftTrk_Scale': maxvariation=0.05
        if systName=='JET_Pileup_OffsetMu': maxvariation=0.05
        if systName=='EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR': maxvariation=0.013
        if systName=='EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR': maxvariation=0.013
        if histName.count('dark'):
            if systName.count('ATLAS_PDF4LHC'): 
                maxvariation=0.045
                for syn,mv in inputMap.iteritems():
                    if systName.count(syn) and maxvariation>abs(mv):
                            maxvariation=abs(mv)
                            break
            if systName.count('MUON_'): maxvariation=0.002
            if systName.count('EG_'): maxvariation=0.002
            if systName.count('EL_'): maxvariation=0.002
        print systName,' max variation: ',maxvariation
        SRNorm=0.0
        BinMax=0.0
        for r in regions:
            binNum = options.binNum
            if options.oneCRBin and not r.count('SR'):
                binNum=1
            scaleUpVarFlat=1.0
            scaleDwVarFlat=1.0
            JERScale=0.0
            if systName.count('JER'):
                flatNomInt=nomMap[r].Integral(1,binNum)
                flatUpInt=sysUpMap[r].Integral(1,binNum)
                flatDwInt=sysDwMap[r].Integral(1,binNum)
                if flatUpInt>flatNomInt:
                    JERScale=1.0
                else:
                    JERScale=-1.0
            # add flat syst for Z in the the W CR
            if (histName.count('Z_') and r.count('_one')) or (histName.count('W_') and r.count('_two')):
                #print histName,r
                flatNomInt=nomMap[r].Integral(1,binNum)
                flatUpInt=sysUpMap[r].Integral(1,binNum)
                flatDwInt=sysDwMap[r].Integral(1,binNum)
                if flatNomInt>0.0:
                    scaleUpVarFlat=(flatUpInt/flatNomInt)
                    scaleDwVarFlat=(flatDwInt/flatNomInt)
                    if abs(scaleUpVarFlat-1.0)>0.1:
                        if scaleUpVarFlat<1.0:
                            scaleUpVarFlat=0.92
                        else:
                            scaleUpVarFlat=1.08
                    if abs(scaleDwVarFlat-1.0)>0.1:
                        if scaleDwVarFlat<1.0:
                            scaleDwVarFlat=0.92
                        else:
                            scaleDwVarFlat=1.08
            for ibin in range(1,binNum+1):
                sysbef=0.0
                nomH=rNewfile.Get(HistName(histName, r,'Nom', ibin))
                if not nomH:
                    print 'could not load: ',HistName(histName, r, 'Nom', ibin)
                    continue
                currentNomV=nomH.GetBinContent(1)
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'High', ibin))
                if not sysBinH:
                    continue
                isModified=False
                if scaleUpVarFlat!=1.0:
                    sysBinH.SetBinContent(1,currentNomV*scaleUpVarFlat)
                    isModified=True
                upVariation=1.0
                if currentNomV>0.0:
                    upVariation=sysBinH.GetBinContent(1)/currentNomV
                if JERScale>0.0 and upVariation<1.0 and upVariation!=0.0:
                    upVariation=1.0/upVariation
                    sysBinH.SetBinContent(1,currentNomV*upVariation)
                    isModified=True
                if r.count('SR') and systName.count('JER'):
                    SRNorm = upVariation
                    BinMax=0.06
                    print 'Setting SRNorm:',SRNorm,' for ',histName
                if SRNorm!=0.0 and SRNorm>1.0 and upVariation<1.0 and upVariation!=0.0:
                    upVariation=1.0/upVariation
                    sysBinH.SetBinContent(1,currentNomV*upVariation)
                    isModified=True
                if maxvariation>0.0 and abs(1.0-upVariation)>maxvariation:
                    if (upVariation-1.0)>0.0:
                        upVariation=1.0+maxvariation
                    else:
                        upVariation=1.0-maxvariation
                    sysBinH.SetBinContent(1,currentNomV*upVariation)
                    isModified=True
                if minvariation>0.0 and abs(1.0-upVariation)<minvariation:
                    if (upVariation-1.0)>0.0:
                        upVariation=1.0+minvariation
                    else:
                        upVariation=1.0-minvariation
                    sysBinH.SetBinContent(1,currentNomV*upVariation)
                    isModified=True
                #if isModified:
                #    updateHist+=[sysBinH]
                sysbef=sysBinH.GetBinContent(1)
                sysBinL=rNewfile.Get(HistName(histName, r, systName+'Low', ibin))
                if not sysBinL:
                    continue
                scaleSyst=sysBinL.GetBinContent(1)
                dwVariation=1.0
                if currentNomV>0.0:
                    dwVariation=sysBinL.GetBinContent(1)/currentNomV
                if SRNorm!=0.0 and SRNorm>1.0 and dwVariation>1.0:
                    dwVariation=1.0/dwVariation
                    sysBinL.SetBinContent(1,currentNomV*dwVariation)
                    isModified=True
                if maxvariation>0.0 and abs(1.0-dwVariation)>maxvariation:
                    if (dwVariation-1.0)>0.0:
                        dwVariation=1.0+maxvariation
                    else:
                        dwVariation=1.0-maxvariation
                    sysBinL.SetBinContent(1,currentNomV*dwVariation)
                    isModified=True
                if minvariation>0.0 and abs(1.0-dwVariation)<minvariation:
                    if (dwVariation-1.0)>0.0:
                        dwVariation=1.0+minvariation
                    else:
                        dwVariation=1.0-minvariation
                    sysBinL.SetBinContent(1,currentNomV*dwVariation)
                    isModified=True

                if systName in systNameToSymmet:
                    sysdiffhalf = (sysbef-scaleSyst)/2.0
                    if sysbef>0.0:
                        scaleSyst=currentNomV/sysbef*currentNomV
                        scaleDwVarFlat=1.0
                        #scaleSystH = (currentNomV+sysdiffhalf)
                        #if abs(scaleSystH - currentNomV) < abs(sysbef-currentNomV):
                        #    sysBinH.SetBinContent(1,scaleSystH)
                        #    scaleSyst = (currentNomV-sysdiffhalf)
                sysBinL.SetBinContent(1,scaleSyst*scaleDwVarFlat)
                #print currentNomV,sysbef,sysBinL.GetBinContent(1)

                # do (up - down)/2 and symmeterize
                updw_over_two = (sysBinH.GetBinContent(1)-sysBinL.GetBinContent(1))/2.0
                if currentNomV>0.0 and abs(updw_over_two/currentNomV)> maxvariation:
                    if updw_over_two>0.0:
                        updw_over_two=maxvariation*currentNomV
                    else:
                        updw_over_two=-1.0*maxvariation*currentNomV
                if (JERScale>0.0 and updw_over_two<0.0) or (JERScale<0.0 and updw_over_two>0.0):
                    if ibin<4:
                        updw_over_two*=-1.0
                sysBinL.SetBinContent(1,currentNomV-updw_over_two)
                sysBinH.SetBinContent(1,currentNomV+updw_over_two)
                
                updateHist+=[sysBinH]
                updateHist+=[sysBinL]
    # write the updated histograms
    for ha in updateHist:
        rNewfile.cd()
        ha.Write(ha.GetName(),ROOT.TObject.kOverwrite)
    rNewfile.Close()
        
def DrawRatio(rfile,options,can,systName,histName,regions):

    #ATLAS.Style()
    nomMap={}
    sysUpMap={}
    sysDwMap={}
    hSaveName=''
    nLoaded=0
    binOrder=[1,3,5,7,9,2,4,6,8,10,11,12,13,14,15,16]
    #binOrder=[1,2,3,4,5,6,7,8,9,10,11]
    if options.ph_ana:
        binOrder=[1,2,3,4,5,6,7,8,9,10,11]
    for r in regions:
        #print r
        binNum = options.binNum
        if options.oneCRBin and not r.count('SR'):
            binNum=1
        hName  =HistName(histName, r, 'Nom', binNum+1)
        hNameUp=HistName(histName, r, 'Up', binNum+1)        
        hNameDw=HistName(histName, r, 'Dw', binNum+1)        
        hSaveName=hName.replace('12Nom_oneEleNegLowSigCR12_obs_cuts','')
        hSaveName=hName.replace('12Nom_oneMuNegCR12_obs_cuts','')
        h=ROOT.TH1F(hName,hName,binNum,0.5,0.5+binNum)
        hsys=ROOT.TH1F(hNameUp,hNameUp,binNum,0.5,0.5+binNum)        
        hsysdw=ROOT.TH1F(hNameDw,hNameDw,binNum,0.5,0.5+binNum)        
        for ibin in range(1,binNum+1):
            nomBinH=rfile.Get(HistName(histName, r, 'Nom', ibin))
            #print r,nomBinH.GetBinContent(1)
            if not nomBinH:
                print 'could not load: ',HistName(histName, r, 'Nom', ibin)
                continue
            else:
                nLoaded+=1
            h.SetBinContent(binOrder[ibin-1], nomBinH.GetBinContent(1))
            h.SetBinError  (binOrder[ibin-1], nomBinH.GetBinError  (1))
            #*nomBinH.GetBinError  (1)
            # up variation
            sysBinH=rfile.Get(HistName(histName, r, systName+'High', ibin))
            #print 'sys: ',r,sysBinH.GetBinContent(1)
            if not sysBinH:
                print 'could not load: ',HistName(histName, r, systName+'High', ibin)
                continue
            hsys.SetBinContent(binOrder[ibin-1], sysBinH.GetBinContent(1))
            hsys.SetBinError  (binOrder[ibin-1], 0.0)
            # down variation
            sysdwBinH=rfile.Get(HistName(histName, r, systName+'Low', ibin))
            if not sysdwBinH:
                print 'could not load: ',HistName(histName, r, systName+'Low', ibin)
                continue
            hsysdw.SetBinContent(binOrder[ibin-1], sysdwBinH.GetBinContent(1))
            hsysdw.SetBinError  (binOrder[ibin-1], 0.0)
            #print r,'down: ',sysdwBinH.GetBinContent(1),' up: ',sysBinH.GetBinContent(1),' nom: ',nomBinH.GetBinContent(1)
        nomMap[r]=h.Clone()
        sysUpMap[r]=hsys.Clone()
        sysDwMap[r]=hsysdw.Clone()

    color=1
    drawOpt=''
    leg=ROOT.TLegend(0.2,0.13,0.4,0.25)
    leg.SetNColumns(2);
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    legr=ROOT.TLegend(0.4,0.13,0.6,0.25)
    legr.SetBorderSize(0)
    legr.SetFillColor(0)
    totalMax=1.0
    totalMin=1.0    
    # create hists and divide
    for r in regions:
        binNum = options.binNum
        if options.oneCRBin and not r.count('SR'):
            binNum=1
        if True:
            SetBinomialErrorRatio(sysUpMap[r],nomMap[r])
            SetBinomialErrorRatio(sysDwMap[r],nomMap[r])
        else:
            sysUpMap[r].Divide(nomMap[r])
            sysDwMap[r].Divide(nomMap[r])
        max1=sysUpMap[r].GetMaximum()
        max2=sysDwMap[r].GetMaximum()
        min1=1.0
        min2=1.0
        for i in range(1,binNum):
            if sysUpMap[r].GetBinContent(1)>0.3 and sysUpMap[r].GetBinContent(i)<min1:
                min1=sysUpMap[r].GetBinContent(1)
            if sysDwMap[r].GetBinContent(1)>0.3 and sysDwMap[r].GetBinContent(i)<min2:
                min2=sysDwMap[r].GetBinContent(1)
        if max1>totalMax:
            totalMax=max1
        if max2>totalMax:
            totalMax=max2
        if min1<totalMin:
            totalMin=min1
        if min2<totalMin:
            totalMin=min2
    # label the bins
    for r in regions:
        binNum = options.binNum
        if not r.count('SR') and options.oneCRBin:
            binNum=1
        if options.ph_ana:
            sysUpMap[r].GetXaxis().SetBinLabel(1,'0.25<M_{jj}<0.5')
            if binNum>1:
                sysUpMap[r].GetXaxis().SetBinLabel(2,'0.5<M_{jj}<1.0')
                sysUpMap[r].GetXaxis().SetBinLabel(3,'1.0<M_{jj}<1.5')
                sysUpMap[r].GetXaxis().SetBinLabel(4,'1.5<M_{jj}')
            continue
        
        sysUpMap[r].GetXaxis().SetBinLabel(1,'0.8<M_{jj}<1.0')
        sysUpMap[r].GetXaxis().SetBinLabel(3,'1<M_{jj}<1.5')
        sysUpMap[r].GetXaxis().SetBinLabel(5,'1.5<M_{jj}<2')
        sysUpMap[r].GetXaxis().SetBinLabel(7,'2<M_{jj}<3.5')
        sysUpMap[r].GetXaxis().SetBinLabel(9,'3.5<M_{jj}')
        if options.nBin==11:
            sysUpMap[r].GetXaxis().SetBinLabel(11,'n_{j}>2')
        else:
            sysUpMap[r].GetXaxis().SetBinLabel(11,'n_{j}>2 1.5-2')
            sysUpMap[r].GetXaxis().SetBinLabel(12,'n_{j}>2 2-3.5')
            sysUpMap[r].GetXaxis().SetBinLabel(13,'n_{j}>2 >3.5')
            sysUpMap[r].GetXaxis().SetBinLabel(14,'Low E_{T}^{miss} 1.5-2')
            sysUpMap[r].GetXaxis().SetBinLabel(15,'Low E_{T}^{miss} 2-3.5')
            sysUpMap[r].GetXaxis().SetBinLabel(16,'Low E_{T}^{miss} >3.5')

    # check the region
    color_vec=[1,2, 3, 4, 5, 6,
               #ROOT.kBlue   -9,
               #ROOT.kGreen  -3,
               #ROOT.kCyan   -9,
               17,
               ROOT.kCyan  ,
               #ROOT.kYellow +2,
               #ROOT.kYellow +1,
               ROOT.kMagenta-3,
               ROOT.kOrange,
               ROOT.kOrange-3,
               ]

    yup=1.1
    if totalMax<1.01:
        yup=1.01
    elif totalMax<1.02:
        yup=1.02
    elif totalMax<1.05:
        yup=1.05
    elif totalMax<1.1:
        yup=1.1
    elif totalMax<1.25:
        yup=1.25
    elif totalMax<1.5:
        yup=1.5
    if abs(1.0-totalMin)>abs(yup-1.0):
        yup=2.0
    ydw=2.0-yup
    # draw
    for r in regions:
        sysUpMap[r].SetStats(0)
        sysUpMap[r].SetLineStyle(1)
        sysUpMap[r].GetYaxis().SetTitle(systName+' / Nominal')
        sysUpMap[r].GetXaxis().SetTitle('Fit Bins [ordered in m_{jj}]')
        sysUpMap[r].GetYaxis().SetRangeUser(ydw,yup)
        sysUpMap[r].SetLineColor(color_vec[color-1])
        sysUpMap[r].SetMarkerColor(color_vec[color-1])
        sysUpMap[r].Draw(drawOpt)
        drawOpt='same'
        leg.AddEntry(sysUpMap[r],(r.replace('X_obs_cuts','')).replace('VBFjetSel_XNom_',''))

        sysDwMap[r].SetStats(0)
        sysDwMap[r].GetYaxis().SetRangeUser(ydw,yup)
        sysDwMap[r].SetLineColor(color_vec[color-1])
        sysDwMap[r].SetMarkerColor(color_vec[color-1])
        sysDwMap[r].SetLineStyle(2)
        sysDwMap[r].Draw(drawOpt)
        if color==1:
            legr.AddEntry(sysUpMap[r],'Up variation')
            legr.AddEntry(sysDwMap[r],'Down variation')
        color+=1
        drawOpt='same'
    leg.Draw()
    legr.Draw()
    can.Update()
    
    GetLegLabel(options,can)
    if options.wait:
        can.WaitPrimitive()
    if options.saveAs:
        print 'Saving: ',hSaveName
        can.SaveAs(hSaveName+systName+"."+options.saveAs)
        
if __name__=='__main__':
    p = OptionParser()

    p.add_option('-i', '--input', type='string', help='input file. Created from plotEvent.py')
    p.add_option('--inputUpdate', type='string', help='input file. Created from plotEvent.py')
    p.add_option('-c', '--compare', type='string', help='Compare any number of input files. Does not support --syst atm. example: --compare rfile1.root,rfile2.root')

    p.add_option('--lumi', type='float', default=139, help='Defines the integrated luminosity shown in the label')
    p.add_option('--batch', action='store_true', default=False, help='Turn on batch mode')    
    p.add_option('--binNum', type='int', default=16, help='number of bins')    
    p.add_option('--nBin', type='int', default=1, help='Defines which bin is plotted')
    p.add_option('--smooth', type='int', default=0, help='Smooth options: 1 average bins, 2 run parabolic smoothing, 3 avg Wln and Zll, 5 determine style of smoothing')    
    p.add_option('-s', '--syst', type='string', default="All", help='NEEDS FIXING. defines the systematics that are plotted. -s all <- will plot all available systematics. Otherwise give a key to the dict in systematics.py')# FIXME
    p.add_option('--pullsFile', type='string', default=None, help='pulls file, print yields')
    p.add_option('-d', '--data', action='store_true', help='Draw data')
    p.add_option('--unBlindSR', action='store_true', help='Unblinds the SR bins')
    p.add_option('--debug', action='store_true', help='Print in debug mode')    
    p.add_option('-r', '--ratio', action='store_true', help='Draw data/MC ratio in case of -i and adds ratios to tables for both -i and -c')
    p.add_option('--yieldTable', action='store_true', help='Produces yield table')
    p.add_option('--wait', action='store_true', help='wait on histogram')    
    p.add_option('--saveAs', type='string', help='Saves the canvas in a given format. example argument: pdf')
    p.add_option('-q', '--quite', action='store_true', help='activates Batch mode')
    p.add_option('--texTables', action='store_true', help='Saves tables as pdf. Only works together with --yieldTable')
    p.add_option('--oneCRBin', action='store_true', help='one CR bin')
    p.add_option('--applyNLOEWK', action='store_true', help='apply NLO EWK to Vg strong')    
    p.add_option('--MGCentralValue', action='store_true', help='apply MG central value')    
    p.add_option('--postFitPickleDir', type='string', default=None, help='Directory of post fit yields pickle files. expects the files end in .pickle')    
    p.add_option('--show-mc-stat-err', action='store_true',  dest='show_mc_stat_err', help='Shows the MC stat uncertainties separately from the data ratio error')
    p.add_option('--ZeroCheck', action='store_true',  dest='ZeroCheck', help='check for negative entry and set to 0')
    p.add_option('--PhotonError', action='store_true',  dest='PhotonError', help='update error for single photon')
    p.add_option('--ph-ana', action='store_true',  dest='ph_ana', help='photon analysis')    
    p.add_option('--combinePlusMinus', action='store_true',  dest='combinePlusMinus', help='Combine the Positive and negative CRs')            
    p.add_option('--plot', default='', help='Plots a variable in a certain region. HFInputAlg.cxx produces these plots with the --doPlot flag . Only works with -i and not with -c. example: jj_mass,SR,1_2_3')
    (options, args) = p.parse_args()

    histNames=["W_strong", "Z_strong", "W_EWK", "Z_EWK", "ttbar"] # "multijet", "eleFakes"
    regions=[
    'VBFjetSel_XNom_SRX_obs_cuts',
    'VBFjetSel_XNom_twoEleCRX_obs_cuts',
    'VBFjetSel_XNom_twoMuCRX_obs_cuts',
    'VBFjetSel_XNom_oneElePosCRX_obs_cuts',
    'VBFjetSel_XNom_oneEleNegCRX_obs_cuts',
    'VBFjetSel_XNom_oneMuPosCRX_obs_cuts',
    'VBFjetSel_XNom_oneMuNegCRX_obs_cuts',
    #'VBFjetSel_XNom_oneElePosLowSigCRX_obs_cuts',
    #'VBFjetSel_XNom_oneEleNegLowSigCRX_obs_cuts',
    ]
    if options.combinePlusMinus:
        regions=[
        'VBFjetSel_XNom_SRX_obs_cuts',
        'VBFjetSel_XNom_twoLepCRX_obs_cuts',
        'VBFjetSel_XNom_oneEleCRX_obs_cuts',
        'VBFjetSel_XNom_oneMuCRX_obs_cuts',
            
        ]
        if options.MGCentralValue:
            regions+=['VBFjetSel_XNom_oneEleLowSigCRX_obs_cuts']
    if options.ph_ana:
        histNames=["Wg_strong", "Zg_strong", "Wg_EWK", "Zg_EWK", "ttbar","ggFH125","VBFHgam125"]
        #histNames=["Wg_strong", "Zg_strong", "Wg_EWK", "Zg_EWK", "ttbar"]
        #histNames=["Zg_strong"]
        #histNames+=["VBFHgamdark125","ggFHgamdark125","VBFHgamdark1000","VBFHgamdark2000","VBFHgamdark3000","VBFHgamdark500","VBFHgamdark80","VBFHgamdark1250","VBFHgamdark1500","VBFHgamdark1750"]
        #histNames=["VBFHgamdark125","ggFHgamdark125","VBFHgamdark1000","VBFHgamdark2000","VBFHgamdark3000","VBFHgamdark500","VBFHgamdark80"]        
        regions=[
        'VBFjetSel_XNom_SRX_obs_cuts',
        'VBFjetSel_XNom_twoLepCRX_obs_cuts',
        'VBFjetSel_XNom_oneEleCRX_obs_cuts',
        ]
    if options.batch:
        ROOT.gROOT.SetBatch(True)
    else:
        import VBFAnalysis.ATLAS as ATLAS
        import VBFAnalysis.Style as Style

    # Load libraries
    if options.smooth<7 and options.smooth>0:
        import HInvPlot.JobOptions as config
        config.loadLibs(ROOT)
    can=DeclareCanvas(options)
    if options.ZeroCheck:
        ZeroCheck()    
    if options.applyNLOEWK:
        applyEWKNLO()
    if options.MGCentralValue:
        MGCentralValue(regions)
    if options.PhotonError:
        PhotonError()    
    rfile=ROOT.TFile(options.input,'READ')
    # read in pulls file and print the yields
    if options.pullsFile!=None:
        #for histName in histNames:
        for histName in ["W_strong","W_EWK","Z_strong", "Z_EWK", "ttbar"]:
            if options.combinePlusMinus:
                PrintPulls(rfile,options,can,histName,['VBFjetSel_XNom_twoLepCRX_obs_cuts'])
            else:
                PrintPulls(rfile,options,can,histName,['VBFjetSel_XNom_twoEleCRX_obs_cuts','VBFjetSel_XNom_twoMuCRX_obs_cuts'])            
        sys.exit(0)
    # which syst
    systName='EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR'
    systToSmooth=[#'EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR',
                  #    'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR',
                  #    'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR',
                      'JET_fJvtEfficiency','JET_JvtEfficiency',
                      'JET_Pileup_OffsetMu',
                      'JET_Pileup_OffsetNPV', # still looks weird. some regions are higher or lower than others
                      'JET_Pileup_PtTerm',
                      'JET_Pileup_RhoTopology',
                      'JET_EffectiveNP_Modelling2',
                      'JET_EffectiveNP_Modelling1',
                      'JET_EffectiveNP_Modelling3',
                      'JET_Flavor_Composition',
                      'JET_JER_DataVsMC_MC16',
                      'JET_JER_EffectiveNP_1',
                      'JET_JER_EffectiveNP_2',
                      'JET_JER_EffectiveNP_3',
                      'JET_JER_EffectiveNP_4',
                      'JET_JER_EffectiveNP_5',
                      'JET_JER_EffectiveNP_6',
                      'JET_JER_EffectiveNP_7',
                      'JET_JER_EffectiveNP_8',
                      'JET_JER_EffectiveNP_9',
                      'JET_JER_EffectiveNP_10',
                      'JET_JER_EffectiveNP_11',
                      'JET_EtaIntercalibration_Modelling',
                      'MET_SoftTrk_Scale',
                      'JET_Flavor_Response',
                      'JET_EtaIntercalibration_TotalStat',
                      'PRW_DATASF', # amanda suggested
                      'MET_SoftTrk_ResoPara',
                      'MET_SoftTrk_ResoPerp',
                      'JET_EffectiveNP_Mixed2',
                      'JET_EffectiveNP_Mixed1',
                      'EG_SCALE_ALL',
                      'EG_RESOLUTION_ALL',
                      'PH_EFF_ID_Uncertainty',
                      'PH_EFF_ISO_Uncertainty',                      
                      ]

    systToSmoothGam=['JET_JER_DataVsMC_MC16',
                      'JET_Pileup_RhoTopology',
                      'JET_Flavor_Composition',
                      'JET_Flavor_Response',
                      'JET_Pileup_OffsetNPV',
                      'JET_Pileup_OffsetMu',
                         'JET_Pileup_PtTerm',
                         'JET_EtaIntercalibration_Modelling',
                         'JET_EtaIntercalibration_TotalStat',
                         'JET_JER_EffectiveNP_1',
                         'JET_JER_EffectiveNP_11',
                         'JET_JER_EffectiveNP_8',
                         'JET_JER_EffectiveNP_10',
                         'JET_JER_EffectiveNP_12restTerm',
                     'JET_EffectiveNP_Modelling2',
                      'JET_EffectiveNP_Modelling1',
                      'JET_EffectiveNP_Modelling3',
                         'EG_RESOLUTION_ALL',
                         'JET_EffectiveNP_Modelling2',
                      'JET_EffectiveNP_Modelling1',
                      'JET_EffectiveNP_Modelling3',
                         'PRW_DATASF','PH_EFF_ISO_Uncertainty']
    systToSmoothGamv2=['ATLAS_PDF4LHC_NLO_30_EV1','ATLAS_PDF4LHC_NLO_30_EV10','ATLAS_PDF4LHC_NLO_30_EV11','ATLAS_PDF4LHC_NLO_30_EV12',
                       'ATLAS_PDF4LHC_NLO_30_EV13','ATLAS_PDF4LHC_NLO_30_EV14','ATLAS_PDF4LHC_NLO_30_EV15','ATLAS_PDF4LHC_NLO_30_EV16',
                       'ATLAS_PDF4LHC_NLO_30_EV17','ATLAS_PDF4LHC_NLO_30_EV18','ATLAS_PDF4LHC_NLO_30_EV19','ATLAS_PDF4LHC_NLO_30_EV2',
                       'ATLAS_PDF4LHC_NLO_30_EV20','ATLAS_PDF4LHC_NLO_30_EV21','ATLAS_PDF4LHC_NLO_30_EV22','ATLAS_PDF4LHC_NLO_30_EV23',
                       'ATLAS_PDF4LHC_NLO_30_EV24','ATLAS_PDF4LHC_NLO_30_EV25','ATLAS_PDF4LHC_NLO_30_EV26','ATLAS_PDF4LHC_NLO_30_EV27',
                       'ATLAS_PDF4LHC_NLO_30_EV28','ATLAS_PDF4LHC_NLO_30_EV29','ATLAS_PDF4LHC_NLO_30_EV3','ATLAS_PDF4LHC_NLO_30_EV30',
                       'ATLAS_PDF4LHC_NLO_30_EV4','ATLAS_PDF4LHC_NLO_30_EV5','ATLAS_PDF4LHC_NLO_30_EV6','ATLAS_PDF4LHC_NLO_30_EV7',
                       'ATLAS_PDF4LHC_NLO_30_EV8','ATLAS_PDF4LHC_NLO_30_EV9','ATLAS_PDF4LHC_NLO_30_alphaS','EG_RESOLUTION_ALL',
                       'EG_SCALE_AF2','EG_SCALE_ALL','JET_BJES_Response','JET_EffectiveNP_Detector1','JET_EffectiveNP_Detector2','JET_EffectiveNP_Mixed1',
                       'JET_EffectiveNP_Mixed2','JET_EffectiveNP_Mixed3','JET_EffectiveNP_Modelling1','JET_EffectiveNP_Modelling2','JET_EffectiveNP_Modelling3',
                       'JET_EffectiveNP_Modelling4','JET_EffectiveNP_Statistical1','JET_EffectiveNP_Statistical2','JET_EffectiveNP_Statistical3','JET_EffectiveNP_Statistical4',
                       'JET_EffectiveNP_Statistical5','JET_EffectiveNP_Statistical6','JET_EtaIntercalibration_Modelling','JET_EtaIntercalibration_NonClosure_highE',
                       'JET_EtaIntercalibration_NonClosure_negEta','JET_EtaIntercalibration_NonClosure_posEta','JET_EtaIntercalibration_TotalStat','JET_Flavor_Composition',
                       'JET_Flavor_Response','JET_JER_DataVsMC_AFII','JET_JER_EffectiveNP_1','JET_JER_EffectiveNP_10','JET_JER_EffectiveNP_11','JET_JER_EffectiveNP_12restTerm',
                       'JET_JER_EffectiveNP_2','JET_JER_EffectiveNP_3','JET_JER_EffectiveNP_4','JET_JER_EffectiveNP_5','JET_JER_EffectiveNP_6','JET_JER_EffectiveNP_7',
                       'JET_JER_EffectiveNP_8','JET_JER_EffectiveNP_9','JET_JvtEfficiency','JET_Pileup_OffsetMu','JET_Pileup_OffsetNPV','JET_Pileup_PtTerm',
                       'JET_Pileup_RhoTopology','JET_PunchThrough_AFII','JET_RelativeNonClosure_AFII','JET_fJvtEfficiency','MET_SoftTrk_ResoPara','MET_SoftTrk_ResoPerp',
                       'MET_SoftTrk_Scale','MUON_ID','MUON_MS','MUON_SAGITTA_RESBIAS','MUON_SAGITTA_RHO','MUON_SCALE','PH_EFF_ID_Uncertainty',
                       'PH_EFF_ISO_Uncertainty','PRW_DATASF','VBF_qqH_200','VBF_qqH_25','VBF_qqH_2jet','VBF_qqH_DphijjPSVarWeights','VBF_qqH_Mjj1000',
                       'VBF_qqH_Mjj120','VBF_qqH_Mjj1500','VBF_qqH_Mjj350','VBF_qqH_Mjj60','VBF_qqH_Mjj700','VBF_qqH_MjjPSVarWeights','VBF_qqH_STJetVeto34','VBF_qqH_tot',]
    systToSmoothTest=['EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR',
            #'MET_SoftTrk_Scale', #smoothed
            #'JET_fJvtEfficiency', #smoothedg
            #'JET_JER_DataVsMC_MC16', #smoothed
            'JET_EtaIntercalibration_Modelling',
            'MET_SoftTrk_ResoPara',
            'MET_SoftTrk_ResoPerp',
            'JET_EffectiveNP_Mixed2',
            'JET_EffectiveNP_Mixed1']
    systToSmoothTest10=['MET_SoftTrk_Scale', #smoothed
            'JET_fJvtEfficiency', #smoothed
            'JET_JER_DataVsMC_MC16', #smoothed
            ]
    systToSmoothTestJETWeird=["JET_JER_EffectiveNP_6","JET_JER_EffectiveNP_5","JET_JER_EffectiveNP_2","JET_JER_EffectiveNP_12restTerm","JET_JER_EffectiveNP_10","JET_JER_EffectiveNP_4","JET_JER_EffectiveNP_7","JET_JER_EffectiveNP_11"]
        
    systToSmoothTestextra=['JET_JER_EffectiveNP_5',
                           'JET_JER_EffectiveNP_6',
                           'JET_JER_EffectiveNP_7restTerm',
                           'JET_JvtEfficiency']
    systToSmoothTestextraA=['JET_Flavor_Composition',
                                'JET_JER_EffectiveNP_7restTerm',
                                'JET_JER_EffectiveNP_3',
                            #'EG_SCALE_ALL',
                             #   'EG_RESOLUTION_ALL',
                                'JET_Pileup_OffsetMu']
    systToSmoothTestextraAll=['JET_JER_EffectiveNP_7restTerm','JET_JER_EffectiveNP_1',
                                  'JET_JER_EffectiveNP_2','JET_JER_EffectiveNP_3',
                                  'JET_JER_EffectiveNP_4','JET_JER_EffectiveNP_5',
                                  'JET_JER_EffectiveNP_6','JET_JER_EffectiveNP_7restTerm',
                                  'MET_SoftTrk_ResoPara','MET_SoftTrk_ResoPerp',
                                  'MET_SoftTrk_Scale','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR',
                                  'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR']
    symmet = ['MET_SoftTrk_ResoPara','MET_SoftTrk_ResoPerp','JET_JER_DataVsMC_MC16','JET_fJvtEfficiency','JET_JvtEfficiency','JET_Flavor_Response','JET_Flavor_Composition','JET_EffectiveNP_Modelling3','JET_EffectiveNP_Modelling1','JET_EffectiveNP_Modelling2','JET_JER_EffectiveNP_7restTerm','JET_JER_EffectiveNP_3','JET_Pileup_OffsetMu','JET_JER_EffectiveNP_1']

    allSyst=[]
    if options.syst=='All':
        import HInvPlot.systematics as vbf_syst
        allSystUpAndDown=vbf_syst.systematics('All').getsystematicsList()
        for s in allSystUpAndDown:
            sSystName=s.rstrip('__1up').rstrip('__1down')
            if sSystName not in allSyst:
                allSyst+=[sSystName]
    elif options.syst=='weird':
        allSyst=systToSmooth
    elif options.syst=='weird2':
        allSyst=systToSmoothTest
    elif options.syst=='weird10':
        allSyst=systToSmoothTest10
    elif options.syst=='weirde':
        allSyst=systToSmoothTestextra
    elif options.syst=='jetweird':
        allSyst=systToSmoothTestJETWeird        
    elif options.syst=='gam':
        allSyst=systToSmoothGam
    elif options.syst=='gamv2':
        allSyst=systToSmoothGamv2
        histNames=["VBFHgamdark2000","VBFHgamdark3000",'VBFHgamdark1250','VBFHgamdark1500','VBFHgamdark1750']
        #symmet=systToSmoothGamv2
    elif options.syst=='met200':
        allSyst=systToSmoothTestextraA
    elif options.syst=='useW':
        allSyst=systToSmoothTestextraAll        
    else:
        allSyst=[options.syst]
    print 'Number of syst:',len(allSyst)
    for systNameA in allSyst:
        for histName in histNames:
            if options.smooth:
                if options.combinePlusMinus:
                    Smooth(rfile,options,can,systNameA,histName,regions+['VBFjetSel_XNom_oneEleLowSigCRX_obs_cuts',],symmet)                    
                else:
                    Smooth(rfile,options,can,systNameA,histName,regions+['VBFjetSel_XNom_oneElePosLowSigCRX_obs_cuts','VBFjetSel_XNom_oneEleNegLowSigCRX_obs_cuts'],symmet)
            if not options.batch:
                DrawRatio(rfile,options,can,systNameA,histName,regions)
            sys.stdout.flush()
    del can
    print 'done'

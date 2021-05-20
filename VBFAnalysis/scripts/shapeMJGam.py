import ROOT
from array import array
#f=ROOT.TFile.Open('/tmp/HFALL_feb18_nomU.root','UPDATE')
#f=ROOT.TFile.Open('/tmp/HFPlotALL_plotvar_feb27U.root','UPDATE')
#f=ROOT.TFile.Open('/tmp/HFALL_doPlot_Nom_mtv5.root','UPDATE')
f=ROOT.TFile.Open('/tmp/hf_mc16ALL_mjj_bins_doPlotv.root','UPDATE')
#f=ROOT.TFile.Open('/tmp/HFALL_doPlot_Nom_tmva.root','UPDATE')

bins=4

#hmultijet_VBFjetSel_1Nom_SR1_obs_cuts
#httbar_VBFjetSel_9Nom_oneMuNegCR9_obs_jj_mass
# h.push_back(new TH1F((name+"_jj_mass").c_str(), (name+"_jj_mass;;").c_str(), 10, 0, 5000));
#      h.push_back(new TH1F((name+"_jj_dphi").c_str(), (name+"_jj_dphi;;").c_str(), 6, 0, 3.0));
#      h.push_back(new TH1F((name+"_met_et").c_str(), (name+"_met_et;;").c_str(), 10, 0, 800));
#      h.push_back(new TH1F((name+"_lepmet_et").c_str(), (name+"_lepmet_et;;").c_str(), 10, 0, 800));

# fake ele
hists=[]
newBinning = array('d',[0.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0, 4000.0, 4500.0, 5000.0 ])
newBinning = array('d',[0.0, 250.0, 500.0, 1000.0, 1500.0, 3000.0 ])
newBinningTMVA = array('d',[0.0, 0.25, 0.6, 0.8, 1.0 ])
newBinningMT = array('d',[0.0, 90.0, 130.0, 200.0, 350.0, 500.0 ])
for reg in ['oneEleCR','oneEleLowSigCR']:
    for ibin in range(1,bins+1):
        print ibin
        hcuts = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_cuts'
        hmjj = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_jj_mass'
        hdphijj = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_jj_dphi'
        hphcen = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_ph_cen'
        hmtgam = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_mtgam'
        htmva = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_tmva'
        print hcuts.replace('X','%s' %ibin)
        mymj = f.Get(hcuts.replace('X','%s' %ibin))
        #mjj=ROOT.TH1F(hmjj.replace('X','%s' %ibin),hmjj.replace('X','%s' %ibin),10, 0, 5000)
        mjj=ROOT.TH1F(hmjj.replace('X','%s' %ibin),hmjj.replace('X','%s' %ibin),len(newBinning)-1, newBinning)
        dphijj=ROOT.TH1F(hdphijj.replace('X','%s' %ibin),hdphijj.replace('X','%s' %ibin),6, 0, 3.0)
        
        mtgam=ROOT.TH1F(hmtgam.replace('X','%s' %ibin),hmtgam.replace('X','%s' %ibin),len(newBinningMT)-1, newBinningMT)
        ph_cen=ROOT.TH1F(hphcen.replace('X','%s' %ibin),hphcen.replace('X','%s' %ibin),5, 0, 1.0)
        tmva=ROOT.TH1F(htmva.replace('X','%s' %ibin),htmva.replace('X','%s' %ibin),len(newBinningTMVA)-1, newBinningTMVA)
        print mymj        
        if bins==10:
            if ibin==1 or ibin==6:
                mtgam.SetBinContent(1,mymj.GetBinContent(1)+mtgam.GetBinContent(1))
                mtgam.SetBinError(1,mymj.GetBinError(1))
            if ibin==2 or ibin==7:
                mtgam.SetBinContent(2,mymj.GetBinContent(1)+mtgam.GetBinContent(2))
                mtgam.SetBinError(2,mymj.GetBinError(1))
            if ibin==3 or ibin==8:
                mtgam.SetBinContent(3,mymj.GetBinContent(1)+mtgam.GetBinContent(3))
                mtgam.SetBinError(3,mymj.GetBinError(1))
            if ibin==4 or ibin==9:
                mtgam.SetBinContent(4,mymj.GetBinContent(1)+mtgam.GetBinContent(4))
                mtgam.SetBinError(4,mymj.GetBinError(1))                                
            if ibin==5 or ibin==10:
                mtgam.SetBinContent(5,mymj.GetBinContent(1)+mtgam.GetBinContent(5))
                mtgam.SetBinError(5,mymj.GetBinError(1))                                
            hists+=[mtgam]
        elif bins==1:
            mtgamFrac=[0.35,0.25,0.35,0.05,0.0]
            i=1
            for ifrac in mtgamFrac:
                mtgam.SetBinContent(i,ifrac*mymj.GetBinContent(1))
                mtgam.SetBinError(i,0.3*ifrac*mymj.GetBinError(1))
                i+=1
            mjjFrac=[0.55,0.39,0.05,0.01]
            i=1
            for ifrac in mjjFrac:
                mjj.SetBinContent(i,ifrac*mymj.GetBinContent(1))
                mjj.SetBinError(i,0.3*ifrac*mymj.GetBinError(1))
                i+=1
            tmvaFrac=[0.55,0.39,0.05,0.01]
            i=1
            for ifrac in tmvaFrac:
                tmva.SetBinContent(i,ifrac*mymj.GetBinContent(1))
                tmva.SetBinError(i,0.3*ifrac*mymj.GetBinError(1))
                i+=1
            dphijjFrac=[0.16,0.16,0.16,0.16,0.16,0.16]
            i=1
            for ifrac in dphijjFrac:
                dphijj.SetBinContent(i,ifrac*mymj.GetBinContent(1))
                dphijj.SetBinError(i,0.3*ifrac*mymj.GetBinError(1))
                i+=1
            hphcenFrac=[0.2,0.2,0.2,0.2,0.2]
            i=1
            for ifrac in hphcenFrac:
                ph_cen.SetBinContent(i,ifrac*mymj.GetBinContent(1))
                ph_cen.SetBinError(i,0.3*ifrac*mymj.GetBinError(1))
                i+=1
            hists+=[mjj,dphijj,tmva,ph_cen,mtgam]
        else:
            mjj.SetBinContent(ibin+1,mymj.GetBinContent(1))
            mjj.SetBinError(ibin+1,mymj.GetBinError(1))
            dphijj.SetBinContent(1,0.5*mymj.GetBinContent(1))
            dphijj.SetBinError(1,0.5*mymj.GetBinError(1))
            tmva.SetBinContent(1,mymj.GetBinContent(1))
            tmva.SetBinError(1,mymj.GetBinError(1))
            hists+=[mjj,dphijj,tmva,ph_cen]


for h in hists:
    f.cd()
    h.SetDirectory(f)
    h.Write()

f.Close()

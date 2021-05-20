import ROOT
import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy
import os,sys

#-----------------------------------------
def Style():
    atlas_style_path='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/'
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()


###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":

    from optparse  import OptionParser
    p = OptionParser()

    p.add_option( '--ipath1',     type='string',      default='/tmp/ZmmgammaEWKH7.root',                 dest='ipath1',      help='Input path 1')
    p.add_option( '--ipath2',     type='string',      default='/tmp/ZmmgammaEWKPy8.root',        dest='ipath2',      help='Input path 2')
    p.add_option( '--var',      type='string',      default='jj_mass',                 dest='var',       help='jj_mass,jet_pt2,njets,njets25,jj_dphi,jj_deta,bosonpt')

    (options, args) = p.parse_args()
    
    Style()
    fH7 = ROOT.TFile.Open(options.ipath1)
    fPy = ROOT.TFile.Open(options.ipath2)
    treeName = 'MiniNtuple'
    h1n = fH7.Get("NumberEvents")
    h2n = fPy.Get("NumberEvents")
    runCutH7='/%s*0.7721' %(h1n.GetBinContent(2))
    runCutPy='/%s*0.7721' %(h2n.GetBinContent(2))

    # selection cuts
    #cuts = '*( truth_jj_mass>100e3  && jet_pt[1]>30e3 && truth_jj_dphi<2.5 && boson_pt[0]>90e3)'
    cuts = '*(truth_jj_mass>250e3 && truth_jj_deta>3.0 && jet_pt[0]>60e3 && jet_pt[1]>50e3 && truth_jj_dphi<2.0 && n_ph15==1 && ph_pt[0]>15e3 && ph_pt[0]<110e3 && phcentrality>0.4 && met_nolep_et>150e3 && met_tst_nolep_ph_dphi>1.8 && j3centrality<0.7 && phcentrality>0.4 && met_tst_dphi_j1>1.0 && met_tst_dphi_j2>1.0 && met_tst_dphi_j1>1.0 &&'
    jet2jCut = '(njets25==2 || njets25==3)'
    jet3jCut = '(njets25==3)'
    
    pvars=['jet_label[0]','jet_label[1]','jet_label[2]']
    jetflavor_settings=[[0,4], [20,24]]
    tH7 = fH7.Get(treeName)
    plts = []
    jetIDNum=-1
    for jetID in ['LF','G']:
        jetIDNum+=1
        n1Flavor = 'IpFlavor_%s' %(jetID)
        pltFlavor = ROOT.TH2F(n1Flavor,n1Flavor,4,0.0,100.0,3,0,4.5)
        for jet in range(1,4):
            n1 = 'Ip_%s_%s' %(jet, jetID)
            print n1            
            plt = ROOT.TH2F(n1,n1,4,0.0,100.0,3,0,4.5)
            cuts2j = cuts+jet2jCut+' && %s>=%s && %s<=%s)' %(pvars[jet-1],jetflavor_settings[jetIDNum][0], pvars[jet-1],jetflavor_settings[jetIDNum][1])
            cuts3j = cuts+jet3jCut+' && %s>=%s && %s<=%s)' %(pvars[jet-1],jetflavor_settings[jetIDNum][0], pvars[jet-1],jetflavor_settings[jetIDNum][1])
            print cuts2j
            if jet==3:
                tH7.Draw('abs(jet_eta[%s]):jet_pt[%s]/1.0e3 >> %s' %(jet,jet,n1),'EventWeight'+cuts3j+runCutH7)            
            else:
                tH7.Draw('abs(jet_eta[%s]):jet_pt[%s]/1.0e3 >> %s '%(jet,jet,n1),'EventWeight'+cuts2j+runCutH7)
                #print 'EventWeight'+cuts2j+runCutH7
                #print 'jet_pt[%s]/1.0e3:abs(jet_eta[%s]) >>'%(jet,jet) +n1
            pltFlavor.Add(plt)
            print 'Inte:',pltFlavor.Integral()
        plts+=[pltFlavor]

    # compute the gluon fraction
    totalJets = plts[1].Clone()
    totalJets.Add( plts[0])
    plts[1].Divide(totalJets)

    # Run pythia8
    pltspy8 = []
    jetIDNum=-1
    tPy = fPy.Get(treeName)
    for jetID in ['LF','G']:
        jetIDNum+=1
        n1Flavor = 'IpPyFlavor_%s' %(jetID)
        pltFlavorPy8 = ROOT.TH2F(n1Flavor,n1Flavor,4,0.0,100.0,3,0,4.5)
        for jet in range(1,4):
            n1 = 'IpPy_%s_%s' %(jet, jetID)
            print n1            
            plt = ROOT.TH2F(n1,n1,4,0.0,100.0,3,0,4.5)
            cuts2j = cuts+jet2jCut+' && %s>=%s && %s<=%s)' %(pvars[jet-1],jetflavor_settings[jetIDNum][0], pvars[jet-1],jetflavor_settings[jetIDNum][1])
            cuts3j = cuts+jet3jCut+' && %s>=%s && %s<=%s)' %(pvars[jet-1],jetflavor_settings[jetIDNum][0], pvars[jet-1],jetflavor_settings[jetIDNum][1])
            if jet==3:
                tPy.Draw('abs(jet_eta[%s]):jet_pt[%s]/1.0e3 >> %s' %(jet,jet,n1),'EventWeight'+cuts3j+runCutPy)            
            else:
                tPy.Draw('abs(jet_eta[%s]):jet_pt[%s]/1.0e3 >> %s '%(jet,jet,n1),'EventWeight'+cuts2j+runCutPy)
            pltFlavorPy8.Add(plt)
            print 'Inte Py8:',plt.Integral()
        pltspy8+=[pltFlavorPy8]

    # pythia8 setup. Then take difference with H7
    # compute the gluon fraction    
    totalJetsPy = pltspy8[1].Clone()
    totalJetsPy.Add( pltspy8[0])
    pltspy8[1].Divide(totalJetsPy)
    pltspy8[1].Add(plts[1],-1.0)
    for i in range(0,pltspy8[1].GetNbinsX()+1):
        for j in range(0,pltspy8[1].GetNbinsY()+1):
            pltspy8[1].SetBinContent(i,j, abs(pltspy8[1].GetBinContent(i,j)))
        
    # just save all jets as the save to avoid any crashes. only using PF jets
    #'gluonFraction_AntiKt4EMTopo'
    #'gluonFractionError_AntiKt4EMTopo' #
    fout = ROOT.TFile('fout_jetflavor.root','RECREATE')
    out_plts=[]
    jet_types=['AntiKt6EMTopo', 'AntiKt4EMTopo', 'AntiKt4LCTopo', 'AntiKt6LCTopo', 'AntiKt4EMPFlow', 'AntiKt6EMPFlow']
    for j in jet_types:
        pltF = ROOT.TH2F('gluonFraction_%s' %(j),'gluonFraction_%s' %(j),4,0.0,100.0,3,0,4.5)
        pltE = ROOT.TH2F('gluonFractionError_%s' %(j),'gluonFractionError_%s' %(j),4,0.0,100.0,3,0,4.5)

        # add the H7
        pltF.Add(plts[1])

        # todo add the difference to Pythia8
        pltE.Add(pltspy8[1])
        
        pltF.SetDirectory(fout)
        pltE.SetDirectory(fout)
        out_plts+=[pltF, pltE]
    
    fout.Write()
    fout.Close()

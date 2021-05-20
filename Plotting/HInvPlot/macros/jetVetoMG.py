import ROOT
import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy
import os,sys,math
import array

#-----------------------------------------
def Style():
    atlas_style_path='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/'
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()

def AddOverflow(h):
    last_bin=h.GetNbinsX()
    last_bin_v = h.GetBinContent(last_bin)+h.GetBinContent(last_bin+1)
    last_bin_e = math.sqrt(h.GetBinError(last_bin)**2+h.GetBinError(last_bin+1)**2)
    h.SetBinContent(last_bin+1,0.0)
    h.SetBinError(last_bin+1,0.0)
    h.SetBinContent(last_bin,last_bin_v)
    h.SetBinError(last_bin,last_bin_e)
    
def RatioHistStyle(r1,options,tighter=False):
    r1.GetXaxis().SetTitle('m_{T}(#gamma+MET) [GeV]')
    if options.var.count('jj_mass'):
        r1.GetXaxis().SetTitle('m_{jj} [GeV]')
    if options.var.count('@jet') or options.var.count('njets25'):
        r1.GetXaxis().SetTitle('N_{jet}')
    if options.var.count('parton_Q[0]'):
        r1.GetXaxis().SetTitle('Parton Q^2')
    if options.var.count('parton_x1[0]'):
        r1.GetXaxis().SetTitle('Parton x1')
    if options.var.count('parton_x2[0]'):
        r1.GetXaxis().SetTitle('Parton x2')
    if options.var.count('parton_Q[1]'):
        r1.GetXaxis().SetTitle('Sub-Leading Parton Q')
    r1.GetYaxis().SetTitle('Var/Nom')        
    r1.GetYaxis().SetRangeUser(0.0,1.199)
    if tighter:
        r1.GetYaxis().SetRangeUser(0.801,1.199)        
    #r1.GetYaxis().SetRangeUser(0.0,2.0)
    r1.GetYaxis().SetNdivisions(505);
    r1.GetYaxis().SetTitleSize(20);
    r1.GetYaxis().SetTitleFont(43);
    r1.GetYaxis().SetTitleOffset(1.55);
    r1.GetYaxis().SetLabelFont(43);
    r1.GetXaxis().SetLabelOffset(0.015);     
    r1.GetYaxis().SetLabelSize(15);
    r1.GetXaxis().SetLabelSize(0.15);    
    r1.GetXaxis().SetTitleSize(20);
    r1.GetXaxis().SetTitleFont(43);
    r1.GetXaxis().SetTitleOffset(3.2);
    r1.GetXaxis().SetLabelFont(42);
    
def getATLASLabels(pad, x, y, text=None, selkey=None):
    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(62)
    l.SetTextSize(0.07)
    l.SetTextAlign(11)
    l.SetTextColor(ROOT.kBlack)
    l.Draw()

    delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]

    if True:
        p = ROOT.TLatex(x+0.14, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.065)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.0f fb^{-1}' %(139e3/1.0e3))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.05)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]
        
    if text != None:

        c = ROOT.TLatex(x, y-0.1, text)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.05)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]
    return labs

def Setup2D(h,can,outname):

    can.cd()
    toth = h.Integral()
    h.Scale(1.0/toth)
    h.GetXaxis().SetTitle('Leading Parton ID')
    h.GetYaxis().SetTitle('Sub-Leading Parton ID')
    h.GetZaxis().SetRangeUser(0.00000001,0.45)
    h.DrawNormalized("colz")
    h.GetZaxis().SetRangeUser(0.00000001,0.45)
    can.Update()
    can.WaitPrimitive()
    raw_input('waiting')
    can.SaveAs(outname)
    
###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":

    from optparse  import OptionParser
    p = OptionParser()

    p.add_option( '--ipath1',     type='string',      default='/tmp/',dest='ipath1',help='Input path 1')
    p.add_option( '--ipath2',     type='string',      default='/tmp/',dest='ipath2',help='Input path 2')
    p.add_option( '--jet-veto-eff', action='store_true',     default=False, dest='jet_veto_eff', help='jet veto eff and not drawing yields')    
    p.add_option( '--var',        type='string',      default='truth_jj_mass', dest='var', help='@jet_pt.size(),parton_x1[0],parton_Q[0],truth_jj_mass,mtgammet')

    (options, args) = p.parse_args()
    
    Style()
    treeName = 'MiniNtuple'
    # selection cuts
    cuts = '*(truth_jj_mass>250e3 && truth_jj_deta>3.8 && jet_pt[0]>80e3 && jet_pt[1]>50e3 && truth_jj_dphi<2.0 && met_nolep_et>150e3 &&'
    #cuts+=' parton_pdgid1[0]>-7 && parton_pdgid1[0]<7 && parton_pdgid2[0]>-7 && parton_pdgid2[0]<7 && '
    #cuts+=' ((parton_pdgid1[0]>-7 && parton_pdgid1[0]<7 && parton_pdgid2[0]>7) || (parton_pdgid2[0]>-7 && parton_pdgid2[0]<7 && parton_pdgid1[0]>7)) && '
    #cuts+=' ((parton_pdgid1[0]>7 && parton_pdgid2[0]>7)) && '
    jet23jCut = '(njets25==2 || njets25==3)'
    jetAlljCut = '(njets25>=2)'
    jet23jCut = '(njets25==2 )'
    cuts23j = cuts+jet23jCut+')'
    #cuts23j = cuts+jetAlljCut+')'
    #cutsAllj = cuts+jet23jCut+')'
    cutsAllj = cuts+jetAlljCut+')'
    GeV='/1.0e3'
    #parton_pdgid1[0]:parton_pdgid2[0]
    #TH2F *hh = new TH2F("hh","hh",30,-6.5,23.5, 30,-6.5,23.5)
    if options.var.count('parton_pdgid'):
        options.var='parton_pdgid1[0]:parton_pdgid2[0]'
        GeV=''
    binning = [0.0, 90.0, 130.0, 200.0, 300.0, 500.0, 1000.0]
    if options.var.count('jj_mass'):
        binning = [0.0,250,500,1000,1500,3000]
        binning = [0.0,250,500, 800,1000,1500,2000,2500,3500,5000]        
    if options.var.count('parton_Q'):
        binning = [0.0,75.0,150,250, 325.0,500, 750.0,1000,1500,2000,2500,3000,3500,5000]#,10000,14000]   
        GeV=''
    if options.var.count('parton_x'):
        binning = [0.0,0.025,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.225,0.25,0.275,0.3,0.325,0.35,0.375,0.4,0.425,0.45,0.5,
                       0.55,0.6,0.65,0.7,0.8,1.0]#,10000,14000]   
        GeV=''
    if options.var.count('@jet_pt.size()') or options.var.count('njets25'):
        binning = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]
        GeV=''
    if options.var.count('boson_eta'):
        binning = [-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5]
        GeV=''
    
    znnFiles=['311429.root','311430.root','311431.root','311432.root']
    wFiles=['311446.root','311448.root','311452.root']
    #wFiles=['311429.root']
    pltsJetVeto = []
    pltsAllJet = []
    plts=[]
    fH7s=[]
    weight=0
    for znnFile in znnFiles:
        fH7 = ROOT.TFile.Open(options.ipath1+znnFile)
        h1n = fH7.Get("NumberEvents")
    
        runCutH7='*139000/%s*crossSection' %(h1n.GetBinContent(2))
        tH7 = fH7.Get(treeName)
    
        n1='Ip_truth_jj_mass%s' %(weight)
        n2='Ip_truth_jj_mass%sALL' %(weight)
        newBinning = array.array('d',binning)
        plt=None
        pltn2=None
        if options.var.count('parton_pdgid'):
            plt = ROOT.TH2F(n1,n1, 30,-6.5,23.5, 30,-6.5,23.5)
            pltn2 = ROOT.TH2F(n2,n2, 30,-6.5,23.5, 30,-6.5,23.5)
        else:
            plt = ROOT.TH1F(n1,n1,len(newBinning)-1,newBinning)
            pltn2 = ROOT.TH1F(n2,n2,len(newBinning)-1,newBinning)
        
        tH7.Draw('%s%s >> %s' %(options.var,GeV,n1),'EventWeightSys[0]%s%s' %(cuts23j,runCutH7))
        tH7.Draw('%s%s >> %s' %(options.var,GeV,n2),'EventWeightSys[0]%s%s' %(cutsAllj,runCutH7))
        AddOverflow(plt)
        AddOverflow(pltn2)
        
        pltsJetVeto+=[plt]
        pltsAllJet+=[pltn2]
        fH7s+=[fH7]
    # sum the histograms up
    newPlt = pltsJetVeto[0].Clone()
    newPltn2 = pltsAllJet[0].Clone()
    for p in range(1,len(pltsJetVeto)):
        newPlt.Add(pltsJetVeto[p])
        newPltn2.Add(pltsAllJet[p])
    plts=[newPlt,newPltn2]

    pltsPy8JetVeto = []
    pltsPy8AllJet = []
    pltspy8=[]
    fPys=[]
    for wFile in wFiles:
        fPy = ROOT.TFile.Open(options.ipath2+wFile)
        
        runCutPy=''
        if fPy:
            h2n = fPy.Get("NumberEvents")
            runCutPy='*139000/%s*crossSection' %(h2n.GetBinContent(2))
        tPy = fPy.Get(treeName)
        n1='Ipy_truth_jj_mass%s' %(weight)
        n2='Ipy_truth_jj_mass%sALL' %(weight)
        newBinning = array.array('d',binning)
        plt=None
        pltn2=None
        if options.var.count('parton_pdgid'):
            plt = ROOT.TH2F(n1,n1,  30,-6.5,23.5, 30,-6.5,23.5)
            pltn2 = ROOT.TH2F(n2,n2,30,-6.5,23.5, 30,-6.5,23.5)
        else:
            plt = ROOT.TH1F(n1,n1,len(newBinning)-1,newBinning)
            pltn2 = ROOT.TH1F(n2,n2,len(newBinning)-1,newBinning)
        tPy.Draw('%s%s >> %s' %(options.var,GeV,n1),'EventWeightSys[0]%s%s' %(cuts23j,runCutPy))
        tPy.Draw('%s%s >> %s' %(options.var,GeV,n2),'EventWeightSys[0]%s%s' %(cutsAllj,runCutPy))
        AddOverflow(plt)
        AddOverflow(pltn2)
        
        fPys+=[fPy]
        pltsPy8JetVeto+=[plt]
        pltsPy8AllJet+=[pltn2]

    # sum the histograms up
    newPy8Plt = pltsPy8JetVeto[0].Clone()
    newPy8Pltn2 = pltsPy8AllJet[0].Clone()
    for p in range(1,len(pltsPy8JetVeto)):
        newPy8Plt.Add(pltsPy8JetVeto[p])
        newPy8Pltn2.Add(pltsPy8AllJet[p])
    pltspy8=[newPy8Plt,newPy8Pltn2]
    
    can = ROOT.TCanvas('stack', 'stack', 800, 500)
    can.cd();          # Go back to the main canvas before defining pad2
    # drawing 2d
    if options.var.count('parton_pdgid'):
        ndmjj=''
        #ndmjj='_mjj2500'
        Setup2D(pltspy8[0],can,'parton_pdgid_W_jetVeto'+ndmjj+'.pdf')
        Setup2D(pltspy8[1],can,'parton_pdgid_W_AllJet'+ndmjj+'.pdf')
        Setup2D(plts[0],   can,'parton_pdgid_Znn_jetVeto'+ndmjj+'.pdf')
        Setup2D(plts[1],   can,'parton_pdgid_Znn_AllJet'+ndmjj+'.pdf')
        sys.exit(0)

    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad

    # for plotting
    color=1
    drawOpt=''
    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);    
    leg_entry=['Jet Veto','No Jet Veto']
    
    leg.Draw()
    for p in plts:
        p.GetYaxis().SetTitle('Arb. Yields')
        p.SetLineColor(color)
        p.SetMarkerColor(color)
        p.Draw(drawOpt)
        leg.AddEntry(p,leg_entry[color-1])
        drawOpt='same'
        color+=1

    leg.Draw()
    texts = getATLASLabels(can, 0.65, 0.88,'')
    for t in texts:
        t.Draw()
    can.cd();
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.3);
    pad2.SetGridy(); # vertical grid
    #pad2.SetGridx(); # vertical grid
    pad2.Draw();
    pad2.cd();       # pad2 becomes the current pad

    ratioplt=[]
    drawOpt='AXIS'
    for p in range(1,len(plts)):
        r1=plts[0].Clone()
        RatioHistStyle(r1,options)
        r1.Divide(r1,plts[1],1,1,"B")
        r1.Draw(drawOpt)
        drawOpt='same'
        r1.Draw(drawOpt)
        ratioplt+=[r1]
    can.Update()
    can.WaitPrimitive()
    outVar=options.var
    if options.var.count('@jet'):
        outVar='n_jet'
    if options.var.count('boson_eta'):
        outVar='boson_eta'
    if options.var.count('parton_Q[0]'):
        outVar='leadPartonQ'
    if options.var.count('parton_Q[1]'):
        outVar='subleadPartonQ'
    if options.var.count('parton_x1[0]'):
        outVar='parton_x1'
    if options.var.count('parton_x2[0]'):
        outVar='parton_x2'
    can.SaveAs('scaleVar_%s.pdf' %(outVar))

    # Parton shower
    if len(pltspy8)>0:
        leg.Clear()
        pad1.cd()
        pltspy8[0].SetLineColor(2)
        pltspy8[0].SetMarkerColor(2)
        leg.AddEntry(plts[0], 'MG Z#rightarrow#nu#nu')
        if '311429' in  wFiles[0]:
            leg.AddEntry(pltspy8[0], 'MG Z#rightarrow#nu#nu NP01')
        elif options.ipath2.count('Wenu'):
            leg.AddEntry(pltspy8[0], 'MG W#rightarrowe#nu')
        else:
            leg.AddEntry(pltspy8[0], 'MG W#rightarrow#mu#nu')
        if options.jet_veto_eff:
            plts[0].GetYaxis().SetTitle('Jet Veto Eff.')
            pltspy8[0].Divide(pltspy8[0],pltspy8[1],1,1,"B")
            plts[0].Divide(plts[0],plts[1],1,1,"B")
        plts[0].Draw()
        pltspy8[0].Draw('same')
        leg.Draw()
        for t in texts:
            t.Draw()
        
        pad2.cd()
        rps = pltspy8[0].Clone()
        rps.Divide(plts[0])
        RatioHistStyle(rps,options,True)
        rps.GetYaxis().SetTitle('W/Z')
        if '311429' in  wFiles[0]:
            rps.GetYaxis().SetTitle('NP01/NP0-4')            
        rps.Draw()
        can.Update()
        can.WaitPrimitive()
        if options.jet_veto_eff:
            outVar='jetVetoEff'+outVar
        can.SaveAs('PSVar_%s.pdf' %(outVar))

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
    
def RatioHistStyle(r1,options):
    r1.GetXaxis().SetTitle('m_{T}(#gamma+MET) [GeV]')
    if options.var.count('jj_mass'):
        r1.GetXaxis().SetTitle('m_{jj} [GeV]')
    r1.GetYaxis().SetTitle('Var/Nom')        
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
###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":

    from optparse  import OptionParser
    p = OptionParser()

    p.add_option( '--ipath1',     type='string',      default='/tmp/700019.root',                 dest='ipath1',      help='Input path 1')
    p.add_option( '--ipath2',     type='string',      default='/tmp/ZmmgammaEWKPy8.root',        dest='ipath2',      help='Input path 2')
    p.add_option( '--var',      type='string',      default='truth_jj_mass',                 dest='var',       help='truth_jj_mass,mtgammet')

    (options, args) = p.parse_args()
    
    Style()
    fH7 = ROOT.TFile.Open(options.ipath1)
    fPy = ROOT.TFile.Open(options.ipath2)
    treeName = 'MiniNtuple'
    h1n = fH7.Get("NumberEvents")
    
    runCutH7='*139000/%s*0.1544' %(h1n.GetBinContent(2))
    runCutPy=''
    if fPy:
        h2n = fPy.Get("NumberEvents")
        runCutPy='*139000/%s*0.1544' %(h2n.GetBinContent(2))

    # selection cuts
    #cuts = '*( truth_jj_mass>100e3  && jet_pt[1]>30e3 && truth_jj_dphi<2.5 && boson_pt[0]>90e3)'
    cuts = '*(truth_jj_mass>250e3 && truth_jj_deta>3.0 && jet_pt[0]>60e3 && jet_pt[1]>50e3 && truth_jj_dphi<2.0 && n_ph15==1 && ph_pt[0]>15e3 && ph_pt[0]<110e3 && phcentrality>0.4 && met_nolep_et>150e3 && met_tst_nolep_ph_dphi>1.8 && j3centrality<0.7 && met_tst_dphi_j1>1.0 && met_tst_dphi_j2>1.0 && met_tst_dphi_j3>1.0 &&'
    cuts = '*(truth_jj_mass>250e3 && truth_jj_deta>3.0 && jet_pt[0]>50e3 && jet_pt[1]>40e3 && truth_jj_dphi<3.0 && n_ph15==1 && ph_pt[0]>10e3 && ph_pt[0]<110e3 && phcentrality>0.4 && met_nolep_et>100e3 && met_tst_nolep_ph_dphi>1.8  &&'
    jet23jCut = '(njets25==2 || njets25==3)'
    #jet23jCut = '(njets25>=2 || njets25==3)'
    jet23jCut = '(njets25==2 )'
    cuts23j = cuts+jet23jCut+')'

    binning = [0.0, 90.0, 130.0, 200.0, 300.0, 500.0, 1000.0]
    if options.var.count('jj_mass'):
        binning = [0.0,250,500,1000,1500,3000]
    
    tH7 = fH7.Get(treeName)
    plts = []
    weightEntries=[0,16,4,12,8,14,6,] # sherpa Vg 292= NLOEWK
    #weightEntries=[0,292] # sherpa Vg 292= NLOEWK
    #weightEntries=[85,80,0,63,53,74,101] # MG LO EWK Vg
    #weightEntries=[0,33,13,7,2,27,12] # Fixed MG LO EWK Vg
    for weight in weightEntries:
        n1='Ip_truth_jj_mass%s' %(weight)
        newBinning = array.array('d',binning)
        plt = ROOT.TH1F(n1,n1,len(newBinning)-1,newBinning)
        #plt = ROOT.TH1F(n1,n1,4,0.0,100.0,3,0,4.5)
        tH7.Draw('%s/1.0e3 >> %s' %(options.var,n1),'EventWeightSys[%s]%s%s' %(weight,cuts23j,runCutH7))
        AddOverflow(plt)
        plts+=[plt]

    pltspy8=[]
    if len(runCutPy)>0:
        tPy = fPy.Get(treeName)
        for weight in weightEntries:
            n1='Ipy_truth_jj_mass%s' %(weight)
            newBinning = array.array('d',binning)
            plt = ROOT.TH1F(n1,n1,len(newBinning)-1,newBinning)
            tPy.Draw('%s/1.0e3 >> %s' %(options.var,n1),'EventWeightSys[%s]%s%s' %(weight,cuts23j,runCutPy))
            AddOverflow(plt)
            pltspy8+=[plt]
            
    can = ROOT.TCanvas('stack', 'stack', 800, 500)
    can.cd();          # Go back to the main canvas before defining pad2
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
    leg_entry=['Nominal','BothUp','BothDw','FacUp','FacDw','RenUp','RenDw','NLOEWK']
    
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
        r1=plts[p].Clone()
        RatioHistStyle(r1,options)
        r1.Divide(plts[0])
        r1.Draw(drawOpt)
        drawOpt='same'
        r1.Draw(drawOpt)        
        ratioplt+=[r1]
    can.Update()
    can.WaitPrimitive()
    can.SaveAs('scaleVar_%s.pdf' %(options.var))

    # Parton shower
    if len(pltspy8)>0:
        leg.Clear()
        pad1.cd()
        pltspy8[0].SetLineColor(2)
        pltspy8[0].SetMarkerColor(2)
        leg.AddEntry(plts[0], 'H7 PS')
        leg.AddEntry(pltspy8[0], 'Py8 PS')

        plts[0].Draw()
        pltspy8[0].Draw('same')
        leg.Draw()
        for t in texts:
            t.Draw()
        
        pad2.cd()
        rps = pltspy8[0].Clone()
        rps.Divide(plts[0])
        RatioHistStyle(rps,options)
        rps.Draw()
        can.Update()
        can.WaitPrimitive()
        can.SaveAs('PSVar_%s.pdf' %(options.var))

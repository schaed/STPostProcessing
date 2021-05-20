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

def AddDiff(hnom,hvar,htot,sign=1.0):
    for i in range(0,hnom.GetNbinsX()+1):
        dif = hvar.GetBinContent(i)-hnom.GetBinContent(i)
        #print i,dif,(htot.GetBinContent(i)-hnom.GetBinContent(i))
        tdif = math.sqrt(dif**2+(htot.GetBinContent(i)-hnom.GetBinContent(i))**2)
        if sign<0:
            tdif*=-1.0
        tdif+=hnom.GetBinContent(i)
        htot.SetBinContent(i,tdif)
    
def RatioHistStyle(r1,options):
    r1.GetXaxis().SetTitle('m_{T}(#gamma+MET) [GeV]')
    if options.var.count('jj_mass'):
        r1.GetXaxis().SetTitle('m_{jj} [GeV]')
    if options.var.count('tmva'):
        r1.GetXaxis().SetTitle('Keras Score')        
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

    p.add_option( '--ipath1',     type='string',      default='/tmp/ZnngammaEWKPy8',                 dest='ipath1',      help='Input path 1')
    p.add_option( '--ipath2',     type='string',      default='/tmp/WgammaEWKPy8',        dest='ipath2',      help='Input path 2')
    p.add_option( '--var',      type='string',      default='truth_jj_mass',                 dest='var',       help='truth_jj_mass,mtgammet,tmva')

    (options, args) = p.parse_args()
    
    Style()
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
    if options.var.count('tmva'):
        binning = [0.0, 0.25, 0.6, 0.8, 1]
    
    # Read in files
    fH7s = []
    plts = []
    treeName = 'MiniNtuple'    
    list_vars = ['Nom','Nom','Nom','Nom']#,'Var1Up','Var1Down','Var3aUp','Var3aDown','Var3bUp','Var3bDown','Var3cUp','Var3cDown','Var2Up','Var2Down']#'Var3bDown','Var3cUp','Var3cDown']
    weights=[64.39285509967885,64.39285509967885,64.39285509967885,64.39285509967885]
    q=0
    for v in list_vars:
        fH7 = ROOT.TFile.Open(options.ipath1+v+'.root')
        fH7s+=[fH7]
        h1n = fH7.Get("NumberEvents")
        #runCutH7='*139000/%s*0.1544' %(h1n.GetBinContent(2))
        runCutH7='*139000/%s*0.1544' %(weights[q])
        if q==1: # we are reweigthing the mjj
            runCutH7+='*(truth_jj_mass*truth_jj_mass/1.0e6*(5.00323e-8) -0.000244716*truth_jj_mass/1.0e3+1.24164)'
        if q==2: # we are reweigthing the lead jet pT
            runCutH7+='*(jet_pt[0]>200e3?0.9 : jet_pt[0]*jet_pt[0]/1.0e6*(3.07166e-5)-0.0106125*jet_pt[0]/1.0e3+1.77941)'
        if q==3: # we are reweigthing the sublead jet pT
            runCutH7+='*(jet_pt[1]>200e3?0.95 : jet_pt[1]*jet_pt[1]/1.0e6*(1.50624e-5)-0.00486096*jet_pt[1]/1.0e3+1.33116)'
        q+=1
        tH7 = fH7.Get(treeName)
        weightEntries=[0] # Fixed MG LO EWK Vg
        for weight in weightEntries:
            n1='Ip_truth_jj_mass%s' %(weight)
            newBinning = array.array('d',binning)
            plt = ROOT.TH1F(n1,n1,len(newBinning)-1,newBinning)
            if options.var.count('tmva'):
                tH7.Draw('%s >> %s' %(options.var,n1),'EventWeightSys[%s]%s%s' %(weight,cuts23j,runCutH7))
            else:
                tH7.Draw('%s/1.0e3 >> %s' %(options.var,n1),'EventWeightSys[%s]%s%s' %(weight,cuts23j,runCutH7))
            AddOverflow(plt)
            plts+=[plt]
            
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
    leg_entry=['Nominal','Reweight m_{jj}','Reweight p_{T}^1','Reweight p_{T}^2'] #list_vars #['Nominal','BothUp','BothDw','FacUp','FacDw','RenUp','RenDw']
    
    leg.Draw()
    total_up=plts[0].Clone()
    total_dw=plts[0].Clone()
    nEntry=1
    nNom = plts[0].Integral(0,1001)
    for p in plts:
        p.GetYaxis().SetTitle('Arb. Yields')
        p.SetLineColor(color)
        p.SetMarkerColor(color)
        p.Scale(nNom/p.Integral(0,1001))
        color+=1
        #if leg_entry[nEntry-1].count('Up'):
        #    p.SetLineStyle(2)
        #    if color>1:
        #        AddDiff(plts[0],p,total_up)
        #    color+=1
        #elif leg_entry[nEntry-1].count('Down'):
        #    if color>1:
        #        AddDiff(plts[0],p,total_dw,-1.0)
        #elif leg_entry[nEntry-1].count('Nom'):
        #    color+=1
                
        p.Draw(drawOpt)
        leg.AddEntry(p,leg_entry[nEntry-1])
        drawOpt='same HIST'
        nEntry+=1
    color+=1
    #total_dw.SetLineStyle(2)
    #total_dw.SetLineColor(color)
    #total_dw.SetMarkerColor(color)
    #total_up.SetLineColor(color)
    #total_up.SetMarkerColor(color)
    #leg.AddEntry(total_up,'Total')

    #total_up.Draw(drawOpt)
    #total_dw.Draw(drawOpt)
    
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
    #plts+=[total_up]
    #plts+=[total_dw]
    for p in range(1,len(plts)):
        r1=plts[p].Clone()
        RatioHistStyle(r1,options)
        r1.Divide(plts[0])
        r1.Draw(drawOpt)
        drawOpt='same HIST'
        r1.Draw(drawOpt)        
        ratioplt+=[r1]
    can.Update()
    can.WaitPrimitive()
    can.SaveAs('py8PSVar_%s.pdf' %(options.var))

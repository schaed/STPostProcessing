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

def GetOtherPlots(options):

    plotW=[]
    fNom = ROOT.TFile.Open(options.ipath2+'.root')
    fUp = ROOT.TFile.Open(options.ipath2+'_ScaleUp.root')
    fDw = ROOT.TFile.Open(options.ipath2+'_ScaleDw.root')
    if not fNom:
        return plotW

    hnomLO = fNom.Get(options.var.replace('_NLO','_LO'))
    hupLO  = fUp.Get(options.var.replace('_NLO','_LO'))
    hdwLO  = fDw.Get(options.var.replace('_NLO','_LO'))
    hnomNLO = fNom.Get(options.var).Clone()
    hupNLO  = fUp.Get(options.var).Clone()
    hdwNLO  = fDw.Get(options.var).Clone()
    hnomNLO.SetDirectory(0)
    hupNLO.SetDirectory(0)
    hdwNLO.SetDirectory(0)
    if options.rebin>1:
        for i in [hnomLO,hnomNLO,hupLO,hupNLO,hdwNLO,hdwLO]:
            i.Rebin(options.rebin)
    # ratio with LO
    hnomNLO.Divide(hnomLO)
    hupNLO.Divide(hupLO)
    hdwNLO.Divide(hdwLO)
    plotW=[hnomNLO,hupNLO,hdwNLO]
    
    return plotW

def RatioHistStyle(r1,options,tighter=False):
    r1.GetXaxis().SetTitle('m_{T}(#gamma+MET) [GeV]')
    if options.var.count('mjj'):
        r1.GetXaxis().SetTitle('m_{jj} [GeV]')
    if options.var.count('H_6'):
        r1.GetXaxis().SetTitle('Sub-lead jet y')
    if options.var.count('H_3'):
        r1.GetXaxis().SetTitle('Sub-lead jet p_{T} [GeV]')
    if options.var.count('H_ptj'):
        r1.GetXaxis().SetTitle('Lead jet p_{T} [GeV]')
    if options.var.count('ptv'):
        r1.GetXaxis().SetTitle('p_{T}^{V} [GeV]')        
    if options.var.count('ptleps'):
        r1.GetXaxis().SetTitle('p_{T}^{V} [GeV]')        
    if options.var.count('ptjets'):
        r1.GetXaxis().SetTitle('p_{T}^{V} [GeV]')        
    if options.var.count('ptg'):
        r1.GetXaxis().SetTitle('p_{T}^{#gamma} [GeV]')        
    if options.var.count('etajj'):
        r1.GetXaxis().SetTitle('#Delta#eta_{jj}')
    if options.var.count('H_13'):
        r1.GetXaxis().SetTitle('#Deltay_{jj}')
    if options.var.count('phijj'):
        r1.GetXaxis().SetTitle('#Delta#phi{jj}')
    r1.GetYaxis().SetTitle('Var/Nom')
    r1.GetYaxis().SetRangeUser(0.751,1.2499)
    if tighter:
        r1.GetYaxis().SetRangeUser(0.9001,1.0999)
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

        #a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.0f fb^{-1}' %(139e3/1.0e3))
        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV')
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

    p.add_option( '--ipath1',     type='string',      default='PostConf/VBFNLO/run291_ZAjj_n',                 dest='ipath1',      help='Input path 1')
    p.add_option( '--ipath2',     type='string',      default='PostConf/VBFNLO/run2780_WAjj',        dest='ipath2',      help='Input path 2')
    p.add_option( '--var',      type='string',      default='H_mjj_NLO',                 dest='var',       help='H_ptv_l_NLO,H_mjj_NLO,H_6_NLO,H_3_NLO,H_ptj_NLO')
    p.add_option( '--rebin',      type='int',      default=1,                 dest='rebin',       help='Value to rebin')

    (options, args) = p.parse_args()
    
    Style()
    fNom = ROOT.TFile.Open(options.ipath1+'.root')
    fUp = ROOT.TFile.Open(options.ipath1+'_ScaleUp.root')
    fDw = ROOT.TFile.Open(options.ipath1+'_ScaleDw.root')

    hnomLO = fNom.Get(options.var.replace('_NLO','_LO'))
    hupLO  = fUp.Get(options.var.replace('_NLO','_LO'))
    hdwLO  = fDw.Get(options.var.replace('_NLO','_LO'))
    hnomNLO = fNom.Get(options.var)
    hupNLO  = fUp.Get(options.var)
    hdwNLO  = fDw.Get(options.var)
    
    if not hnomNLO:
        for k in fNom.GetListOfKeys():
            print k.GetName()
        print 'Pick from above'    
        sys.exit(0)
    if options.rebin>1:
        for i in [hnomLO,hnomNLO,hupLO,hupNLO,hdwNLO,hdwLO]:
            i.Rebin(options.rebin)

    can = ROOT.TCanvas('stack', 'stack', 800, 500)
    can.cd();          # Go back to the main canvas before defining pad2
    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad
    
    # ratio with LO
    hnomNLO.Divide(hnomLO)
    hnomNLO.Fit('pol2')
    hnomNLO.Draw()
    can.Update()
    can.WaitPrimitive()
    hupNLO.Divide(hupLO)
    hdwNLO.Divide(hdwLO)
    plts=[hnomNLO,hupNLO,hdwNLO]
    for i in range(0,hnomNLO.GetNbinsX()+1):
        #hnomNLO.SetBinError(i,0.03*hnomNLO.GetBinContent(i))
        hnomNLO.SetBinError(i,0.0*hnomNLO.GetBinContent(i))        
        hupNLO.SetBinError(i,0)
        hdwNLO.SetBinError(i,0.0)
    
    # for plotting
    color=1
    drawOpt='HIST E'
    leg = ROOT.TLegend(0.65, 0.05, 0.98, 0.35)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);
    leg_entry=['Nominal','BothUp','BothDw']
    
    leg.Draw()
    for p in plts:
        p.GetYaxis().SetTitle('NLO / LO QCD Corrections')
        p.SetLineColor(color)
        #p.GetYaxis().SetRangeUser(0.651,1.2499)
        p.GetYaxis().SetRangeUser(0.51,1.499)
        p.SetMarkerSize(0)
        p.SetMarkerColor(color)
        p.Draw(drawOpt)
        leg.AddEntry(p,leg_entry[color-1])
        drawOpt='same HIST'
        color+=1

    leg.Draw()
    labeltext='#gamma+Z#rightarrow#nu#nu'
    if options.ipath1.count('W'):
        labeltext='#gamma+W#rightarrowl#nu'
    if options.ipath1.count('jj_l'):
        labeltext='#gamma+Z#rightarrowll'
    texts = getATLASLabels(can, 0.65, 0.88,labeltext)
    for t in texts:
        t.Draw()
    can.cd();
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.3);
    pad2.SetGridy(True); # vertical grid
    pad2.Draw();
    pad2.cd();       # pad2 becomes the current pad

    ratioplt=[]
    drawOpt='AXIS'
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
    can.SaveAs('scaleVarVBFNLO_%s.pdf' %(options.var))

    ## Try reading in the W file
    pltWs = GetOtherPlots(options)
    if len(pltWs)==0:
        sys.exit(0)

    # Divide W/Z
    for ip in range(0,len(plts)):
        pltWs[ip].Divide(plts[ip])

    pad1.cd();
    color=1
    drawOpt=' HIST'
    leg.Clear()
    for p in pltWs:
        p.GetYaxis().SetTitle('W/Z k-factor')
        if options.ipath2.count('ZAjj'):
            p.GetYaxis().SetTitle('Zll/Znn k-factor')
        p.SetLineColor(color)
        p.GetYaxis().SetRangeUser(0.9001,1.09999)
        p.SetMarkerSize(0)        
        p.SetMarkerColor(color)
        p.Draw(drawOpt)
        leg.AddEntry(p,leg_entry[color-1])
        drawOpt='same HIST'        
        color+=1
    leg.Draw()
    texts = getATLASLabels(can, 0.65, 0.88,'W/Z')
    if options.ipath2.count('ZAjj'):
        texts = getATLASLabels(can, 0.65, 0.88,'Zll/Znn')        
    for t in texts:
        t.Draw()
    ratiopltW=[]
    drawOpt='AXIS'
    pad2.cd();
    for p in range(1,len(plts)):
        r1=pltWs[p].Clone()
        RatioHistStyle(r1,options,True)
        r1.Divide(pltWs[0])
        if options.ipath2.count('WAjj'):
            r1.GetYaxis().SetTitle('W / Z corr.')
        if options.ipath2.count('ZAjj'):
            r1.GetYaxis().SetTitle('Zll / Znn corr.')            
        r1.Draw(drawOpt)
        drawOpt='same HIST'
        r1.Draw(drawOpt)        
        ratiopltW+=[r1]
    can.Update()
    can.WaitPrimitive()
    if options.ipath2.count('ZAjj'):
        can.SaveAs('scaleVarVBFNLOZllZnn_%s.pdf' %(options.var))        
    else:
        can.SaveAs('scaleVarVBFNLOWZ_%s.pdf' %(options.var))

#!/usr/bin/env python

import os,sys
import re
import sys
import math
import copy

from optparse import OptionParser

p = OptionParser(usage="usage: <path:ROOT file directory>", version="0.1")

p.add_option('-n',             type='int',    default=0,             dest='nevent')
p.add_option('--hscale',       type='float',    default=0.13,          dest='hscale')
p.add_option('--hscalealt',       type='float', default=0.13,          dest='hscalealt')
p.add_option('--year',         type='int',    default=2016,          dest='year')
p.add_option('--hmass',        type='string', default='125',         dest='hmass')

p.add_option('--selkey',       type='string', default='pass_sr_hipt_1j_eu', dest='selkey')
p.add_option('--algkey',       type='string', default='plotEvent',   dest='algkey')
p.add_option('--vars',         type='string', default=None,          dest='vars')
p.add_option('--outdir',       type='string', default=None,          dest='outdir')

p.add_option('--pref',         type='string', default=None,          dest='pref')
p.add_option('--signal',       type='string', default='higgs',       dest='signal',help='options: higgs, susy, whww, or gamd')
p.add_option('--extrasignal',  type='string', default=None,          dest='extrasignal',help='options: higgs, whww or gamd')
p.add_option('--syst',         type='string', default='Nominal',     dest='syst')
p.add_option('--syst-sel',     type='string', default='Nominal',     dest='syst_sel')
p.add_option('--syst-see',     type='string', default=None,          dest='syst_see')
p.add_option('--sf-file',      type='string', default=None,          dest='sf_file')
p.add_option('--do-nf',        type='string', default=None,          dest='do_nf')
p.add_option('--extract-sig',  type='string', default=None,          dest='extract_sig')
p.add_option('--syst-table',   type='string', default=None,          dest='syst_table')

p.add_option('--int-lumi',     type='float',  default=36207.66,       dest='int_lumi') # 2017: 44307.4, 2018: 58.45
p.add_option('--ymin',         type='float',  default=None,          dest='ymin')
p.add_option('--ymax',         type='float',  default=None,          dest='ymax')
p.add_option('--xmax',         type='float',  default=None,          dest='xmax')
p.add_option('--xmin',         type='float',  default=None,          dest='xmin')

p.add_option('--blind',         action='store_true', default=False,   dest='blind')
p.add_option('--preliminary',   action='store_true', default=False,   dest='preliminary')
p.add_option('--normalizeBkg',  action='store_true', default=False,   dest='normalizeBkg')
p.add_option('--normalizeWBkg', action='store_true', default=False,   dest='normalizeWBkg')
p.add_option('--getMJNF',       action='store_true', default=False,   dest='getMJNF')
p.add_option('--madgraph',      action='store_true', default=False,   dest='madgraph')
p.add_option('--do-eps',        action='store_true', default=False,   dest='do_eps')
p.add_option('--do-c',          action='store_true', default=False,   dest='do_c')
p.add_option('--do-pdf',        action='store_true', default=False,   dest='do_pdf')
p.add_option('--do-root',       action='store_true', default=False,   dest='do_root')
p.add_option('--do-logy',       action='store_true', default=False,   dest='do_logy')
p.add_option('--no-logy',       action='store_true', default=False,   dest='no_logy')
p.add_option('--mg-ratio',       action='store_true', default=False,  dest='mg_ratio')
#p.add_option('--do-fakeE',       action='store_true', default=False,  dest='do_fakeE')
p.add_option('--draw-norm',     action='store_true', default=False,   dest='draw_norm')
p.add_option('--do-ks',     action='store_true', default=False,   dest='do_ks')
p.add_option('--do-ratio',      action='store_true', default=False,   dest='do_ratio')
p.add_option('--force-ratio',   action='store_true', default=False,   dest='force_ratio')
p.add_option('--stack-signal',  action='store_true', default=False,   dest='stack_signal')
p.add_option('--ph-ana',        action='store_true', default=False,   dest='ph_ana')
p.add_option('--doVjetMjjRW',   action='store_true', default=False,   dest='doVjetMjjRW')
p.add_option('--no-signal',     action='store_true', default=False,   dest='no_signal')

p.add_option('--debug',         action='store_true', default=False,   dest='debug')
p.add_option('--wait',          action='store_true', default=False,   dest='wait')
p.add_option('--save',          action='store_true', default=False,   dest='save')
p.add_option('--save-algkey',   action='store_true', default=False,   dest='save_algkey')
p.add_option('--syst-fakes',    type='int',          default=0,       dest='syst_fakes')
p.add_option('--syst-trkmet',   type='int',          default=0,       dest='syst_trkmet')
p.add_option('--no-underflow',  action='store_true', default=False,   dest='no_underflow')
p.add_option('--show-mc-stat-err',  action='store_true', default=False,   dest='show_mc_stat_err')
p.add_option('--add-fakeE',  action='store_true', default=False,   dest='add_fakeE')

p.add_option('--syst-type',     type='string', default='All',           dest='syst_type', help='SigTheory, All, or MJsyst')
p.add_option('--draw-syst',       action='store_true', default=False,   dest='draw_syst')
p.add_option('--make-syst-table', action='store_true', default=False,   dest='make_syst_table')

p.add_option('--atlas-style', dest='atlas_style_path', default="/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/")

# Allow canvas size and legend coords to be overriden on the command line.  0.51, 0.60, 0.915, 0.855)
p.add_option('--legend-coords', dest='legend_coords', nargs=4, default=(0.55, 0.60, 0.94, 0.9), type=float)
p.add_option('--canvas-size', dest="canvas_size", nargs=2, default=(500, 500), type=int)

# Allow a vertical dashed line to be drawn over the plot.
p.add_option('--vertical-line', dest='vertical_line', default=None, type=float, help='Draw a vertical line on the plot.')

# Number of legend columns; defaults to two. Set to one to restore old legend format.
p.add_option('--legend-cols', dest='legend_cols', default=2, type=int, help='Number of columns to split the legend.')

(options, args) = p.parse_args()

# Make this a global variable from the argument parser.
atlas_style_path = options.atlas_style_path

import ROOT
import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy
import HInvPlot.systematics as import_syst

#config.setPlotDefaults(ROOT)

if not options.wait:
    ROOT.gROOT.SetBatch(True)

log = config.getLog('drawStack.py', debug=options.debug)
mysyst=None
# List of plots to symmeterize
symm_list=[]

mysyst = import_syst.systematics(options.syst_type, options.ph_ana, options.doVjetMjjRW)
mysystOneSided = import_syst.systematics('OneSidedDown', options.ph_ana, options.doVjetMjjRW)
#add asymetric uncertainties
for key,v in mysystOneSided.getsystematicsOneSidedMap().iteritems():
    if (v in mysyst.getsystematicsList()):
        symm_list+=[key]
print 'symm_list:',symm_list
#-----------------------------------------
def Style():
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()

#-------------------------------------------------------------------------
def getSelKeyPath():

    if options.save_algkey:
        return '%s_%s' %(options.selkey, options.algkey)
    return options.selkey

#-------------------------------------------------------------------------
def getSelKeyLabel(selkey):

    proc = None
    decay = 'Invis'
    if selkey != None: # and selkey.count('hww') or selkey.count('lowmet'):
        if True:
            if selkey.count('_nn'): proc = 'VBF #it{h}#rightarrow%s' %decay
            elif selkey.count('_ll'): proc = '#it{Z}_{ll}'#'#it{Z}#rightarrow ll'
            elif selkey.count('_ee'): proc = '#it{Z}_{#it{ee}}' #'#it{Z}#rightarrow ee'
            elif selkey.count('_eu'): proc = '#it{e#mu}'
            elif selkey.count('_em'): proc = '#it{W}_{#it{e^{+}#nu}}'#'W#rightarrow e^{-}#nu'^{high}
            elif selkey.count('_ep'): proc = '#it{W}_{#it{e^{-}#nu}}' #^{high}
            elif selkey.count('_uu'): proc = '#it{Z}_{#it{#mu#mu}}' #'Z#rightarrow#mu#mu'
            elif selkey.count('_l'): proc = 'W#rightarrow l#nu'
            elif selkey.count('_e'): proc = '#it{W}_{#it{e#nu}}'#'W#rightarrow e#nu'^{high}
            elif selkey.count('_u'): proc = '#it{W}_{#it{#mu#nu}}'#it{W}#rightarrow#it{#mu#nu}'
        if selkey.count('gam'):
            proc+='+#gamma'
            if selkey.count('_nn'): proc = 'VBF #gamma #it{h}#rightarrow%s' %decay
            
        if selkey.count('LowMETQCD_'):  proc += ', Low MET QCD'
        elif selkey.count('LowMETQCDFJVT_'):  proc += ', Low MET QCD'
        elif selkey.count('LowMETQCDVR'):  proc += ', Low MET,2.5<#Delta#eta<3.8 QCD'
        elif selkey.count('LowMETQCDSR'): proc = 'Low #it{E}_{T}^{miss}' #proc += ', Low MET QCD, N_{jet}=2'
        elif selkey.count('mjjLow200_'):  proc = 'Low #it{m}_{jj}' #proc += ', 0.2<m_{jj}<0.8TeV'
        elif selkey.count('deta25_'):  proc += ', 2.5<#Delta#eta<3.8'
        elif selkey.count('lowmet_'):  proc += ', Low #it{E}_{T}^{miss}'
        elif selkey.count('revfjvt_'):  proc += ', Reverse FJVT'
        elif selkey.count('revphcen_'):  proc += ', Reverse #gamma Cen.'
        elif selkey.count('njgt2lt5_'):  proc += ',2<#it{N}_{jet}<5'
        elif selkey.count('njgt3lt5_'):  proc += ',3<#it{N}_{jet}<5'
        elif selkey.count('njgt2_'):  proc += ',#it{N}_{jet} #geq 3'
        elif selkey.count('anasusy_'):  proc += ',2#leq#it{N}_{jet} #leq 5'            
        elif selkey.count('njgt3_'):  proc += ',#it{N}_{jet} #geq 4'
        elif selkey.count('phijj3'):  proc += ',2.0<|#Delta#phi|<2.5'
        if selkey.count('nj2'):  proc += ',#it{N}_{jet}=2'            
        if selkey.count('sr_'):  proc += ' SR'
        elif selkey.count('wcr'):
            if 'anti' in selkey:
                proc += ' anti-ID'
            else:
                proc += ' CR'
        elif selkey.count('zcr'): proc += ' CR'
        if selkey.count('FJVT_'):  proc += ',f-jvt'
        if selkey.count('LowMETQCDSR'): proc = 'Low #it{E}_{T}^{miss} CR' #proc += ', Low MET QCD, N_{jet}=2'
        elif selkey.count('mjjLow200_'):  proc = 'Low #it{m}_{jj} CR' #proc += ', 0.2<m_{jj}<0.8TeV'
    return proc

#-------------------------------------------------------------------------
def getATLASLabels(pad, x, y, text=None, selkey=None):

    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(72)
    l.SetTextSize(0.07)
    l.SetTextAlign(11)
    l.SetTextColor(ROOT.kBlack)
    l.Draw()

    delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]

    if True:
        typeN='Internal'
        if options.preliminary:
            typeN='Preliminary'
        p = ROOT.TLatex(x+0.15, y, ' '+typeN) #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.065)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{#it{s}} = 13 TeV, %.0f fb^{-1}' %(options.int_lumi/1.0e3))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.05)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]

    proc = getSelKeyLabel(selkey)
    if proc != None:

        c = ROOT.TLatex(x, y-0.1, proc)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.05)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]

    return labs

#-------------------------------------------------------------------------
def getHistPars(hist):

    labels = {
        #
        # Kinematics histograms
        #
        # Note on option: LtoRCut 0 cuts for values > thr
        #                         1 cuts for values < thr
        #                         2 bin-by-bin significance
        #                         3 tried to combine bins to one value - use with care especially with many bins
        #                         4 adds every two bins together
        'jetEta0': {'xtitle':'Leading jet #it{#eta}'  ,           'ytitle':'Events', 'rebin':5}, #5
        'jet0Phi': {'xtitle':'Leading jet #it{#phi}'  ,           'ytitle':'Events', 'rebin':2},
        'jetPt0' : {'xtitle':'#it{p}_{T}^{jet 1} [GeV]',          'ytitle':'Events / 10 GeV', 'rebin':2, 'LtoRCut':0},#,'xmax':150},
        'jetHT' : {'xtitle':'H_{T} [GeV]',          'ytitle':'Events', 'rebin':2, 'logy':True, 'LtoRCut':0},
        'jetEta1': {'xtitle':'Sub-Leading jet #it{#eta}'  ,       'ytitle':'Events', 'rebin':5},
        'jet1Phi': {'xtitle':'Sub-Leading jet #it{#phi}'  ,       'ytitle':'Events', 'rebin':2},
        'jetPt1' : {'xtitle':'#it{p}_{T}^{jet 2} [GeV]',          'ytitle':'Events / 10 GeV', 'rebin':5, 'LtoRCut':0},
        'j0jvt' : {'xtitle':'Leading jet JVT',          'ytitle':'Events', 'rebin':1,'ymin':0.1, 'rebin':1, 'logy':True},
        'j1jvt' : {'xtitle':'sub-Leading jet JVT',          'ytitle':'Events', 'rebin':1,'ymin':0.1, 'rebin':1, 'logy':True},
        'j0fjvt' : {'xtitle':'Leading jet f-JVT',          'ytitle':'Events', 'rebin':1,'ymin':0.1, 'logy':True, 'LtoRCut':0},
        'j1fjvt' : {'xtitle':'sub-Leading jet f-JVT',          'ytitle':'Events', 'rebin':1,'ymin':0.1, 'logy':True, 'LtoRCut':0},
        'j0timing' : {'xtitle':'Leading jet timing [ns]',          'ytitle':'Events', 'rebin':1,'ymin':0.1, 'logy':True},
        'j1timing' : {'xtitle':'sub-Leading jet timing [ns]',          'ytitle':'Events', 'rebin':1,'ymin':0.1, 'logy':True},
        'n_jet'   : {'xtitle':'Number of Jets',               'ytitle':'Events',  'ymin':0.1, 'logy':False, 'LtoRCut':1, 'xmax':9.0},
        'n_jet_fwd'   : {'xtitle':'Number of extra Jets |eta|>2.5',               'ytitle':'Events', 'rebin':0},
        'n_jet_fwdj'   : {'xtitle':'Number of Jets outside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_jet_fwdj30'   : {'xtitle':'Number of Jets outside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_jet_fwdj40'   : {'xtitle':'Number of Jets outside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_jet_fwdj50'   : {'xtitle':'Number of Jets outside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_jet_cen'   : {'xtitle':'Number of extra Jets |eta|<2.5',               'ytitle':'Events', 'rebin':0},
        'n_jet_fwd'   : {'xtitle':'Number of extra Jets |eta|>2.5',               'ytitle':'Events', 'rebin':0},
        'n_jet_cenj'   : {'xtitle':'Number of Jets inside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_jet_cenj30'   : {'xtitle':'Number of Jets inside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_jet_cenj40'   : {'xtitle':'Number of Jets inside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_jet_cenj50'   : {'xtitle':'Number of Jets inside tagging jets',               'ytitle':'Events', 'rebin':0},
        'n_bjet'  : {'xtitle':'Number of B Jets',             'ytitle':'Events', 'rebin':0,'ymin':0.1, 'logy':False,'LtoRCut':1},
        #'tmva'  : {'xtitle':'BDT Score',          'ytitle':'Events', 'rebin':0,'LtoRCut':0,'xmin':-0.4,'xmax':0.6,'ymin':0.01},
        #'tmva'  : {'xtitle':'Keras ANN Score',    'ytitle':'Events', 'rebin':10,'LtoRCut':0,'xmin':0.0,'ymin':0.1},
        'tmva'  : {'xtitle':'Keras ANN Score',    'ytitle':'Events', 'rebin':0,'LtoRCut':2,'xmin':0.0,'ymin':0.1},        
        'bcid'  : {'xtitle':'BCID',             'ytitle':'Events', 'rebin':0,'LtoRCut':1},
        'BCIDDistanceFromFront'  : {'xtitle':'Distance from front of Train','ytitle':'Events', 'rebin':0,'LtoRCut':1},
        'averageIntPerXing'  : {'xtitle':'Average Interactions per Xing (#mu)',             'ytitle':'Events', 'rebin':4,'LtoRCut':1},
        'lb'  : {'xtitle':'Lumi block','ytitle':'Events', 'rebin':0,'LtoRCut':1}, 
        'n_vx'  : {'xtitle':'Recontructed Vertices (N_{PV})','ytitle':'Events', 'rebin':0,'LtoRCut':1},
        'JetEtaPt25'  : {'xtitle':'Jet #it{#eta} wth 25<#it{p}_{T}<35 GeV','ytitle':'Events', 'rebin':2,'LtoRCut':1},
        'JetEtaPt35'  : {'xtitle':'Jet #it{#eta} wth 35<#it{p}_{T}<55 GeV','ytitle':'Events', 'rebin':2,'LtoRCut':1},                 
        'JetEtaPt55'  : {'xtitle':'Jet #it{#eta} wth 55<#it{p}_{T} GeV','ytitle':'Events', 'rebin':5,'LtoRCut':1},                 
        'JetEMECvsBCIDPosPt25'  : {'xtitle':'Jet Number jets wth 25<#it{p}_{T}<35 GeV','ytitle':'Events', 'rebin':0,'LtoRCut':1},
        'JetEMECvsBCIDPosPt35'  : {'xtitle':'Jet #it{#eta} wth 35<#it{p}_{T}<55 GeV','ytitle':'Events', 'rebin':0,'LtoRCut':1},                 
        'JetEMECvsBCIDPosPt55'  : {'xtitle':'Jet #it{#eta} wth 55<#it{p}_{T} GeV','ytitle':'Events', 'rebin':0,'LtoRCut':1},                 

        'lepPt0'   : {'xtitle':'Lepton #it{p}_{T} [GeV]', 'ytitle':'Events', 'rebin':5,},#'xmax': 200,
        'baseMuPt'   : {'xtitle':'Base #it{p}_{T}^{#mu} [GeV]', 'ytitle':'Events', 'rebin':5},
        'baseMuEta'   : {'xtitle':'Base #it{#eta}_{#mu}', 'ytitle':'Events', 'rebin':5},
        'baseElPt'   : {'xtitle':'Electron #it{p}_{T} [GeV]', 'ytitle':'Events', 'rebin':4, 'xmax': 600, 'logy': True},
        'elec_num_pt'   : {'xtitle':'Id Electron #it{p}_{T} [GeV]', 'ytitle':'Events', 'rebin':5},
        'muon_den_pt'   : {'xtitle':'Anti-Id Muon #it{p}_{T} [GeV]', 'ytitle':'Events', 'rebin':0},
        'lepEta' : {'xtitle':'Lepton #it{#eta} [GeV]',              'ytitle':'Events', 'rebin':0,    'ymin':0.0},
        'lepPhi' : {'xtitle':'Lepton #it{#phi} [GeV]',              'ytitle':'Events', 'rebin':0,    'ymin':0.0},
        'dphill' : {'xtitle':'#Delta#it{#phi}_{ll}',                 'ytitle':'Events / 0.2 rad', 'rebin':5,  'ymin':0.01},
        'jj_dphi' : {'xtitle':'#Delta#it{#phi}_{jj}',                 'ytitle':'Events / 0.4 rad', 'rebin':4,  'ymin':0.01, 'xmax':4.0}, #,'ymax':2000.01,'ymax':5500.01, 'ymax':4200.01 , 'ymax':239.99 'ymax':2000.01,
        #'jj_dphi' : {'xtitle':'#Delta#it{#phi}_{jj}',                 'ytitle':'Events / 0.2 rad', 'rebin':2,  'ymin':0.01, 'xmax':4.0}, #,'ymax':2000.01,'ymax':5500.01, 'ymax':4200.01 , 'ymax':239.99 'ymax':2000.01,        
        'met_soft_tst_et'    : {'xtitle':'#it{E}_{T}^{miss,soft} [GeV]',                 'ytitle':'Events / 5 GeV', 'rebin':1,  'ymin':0.1, 'logy':True, 'LtoRCut':1},
        'met_tst_et'    : {'xtitle':'#it{E}_{T}^{miss} [GeV]',                 'ytitle':'Events / 20 GeV', 'rebin':2,  'ymin':0.1, 'logy':False,'xmin':0,'LtoRCut':0,'xmin':100},#'xmax':500, 
        'met_tst_phi'    : {'xtitle':'#it{E}_{T}^{miss} #it{#phi}',                 'ytitle':'Events', 'rebin':4,  'ymin':0.01, 'logy':False},
        'met_tst_nolep_et'    : {'xtitle':'#it{E}_{T}^{miss} (without leptons) [GeV]',              'xmax':500,    'ytitle':'Events / 50 GeV', 'rebin':5, 'logy':False},#,'xmin':100,}, #'ymin':50.1,'ymax':30000 # for Z 'xmax':500,  'ymin':5.01, 'ymax':3000, ###'xmin':200,  'ymin':50.1,'ymax':30000, 'xmax':500,'xmin':200,  'ymin':50.1,'ymax':25000,
        'met_tst_nolep_phi'    : {'xtitle':'#it{E}_{T}^{miss} (without leptons) #it{#phi}',                 'ytitle':'Events', 'rebin':4,  'ymin':0.01, 'logy':False},
        'mll'    : {'xtitle':'#it{m}_{ll} [GeV]'  ,                    'ytitle':'Events / 5 GeV', 'rebin':2,  'ymin':0.001, 'xmax':200.0},
        'mlg'    : {'xtitle':'#it{m}_{l#gamma} [GeV]'  ,                    'ytitle':'Events / 5 GeV', 'rebin':4,  'ymin':0.001, 'xmax':500.0},        
        'mllg'    : {'xtitle':'#it{m}_{ll#gamma} [GeV]'  ,                    'ytitle':'Events / 5 GeV', 'rebin':4,  'ymin':0.001, 'xmax':500.0},
        'jj_mass'    : {'xtitle':'#it{m}_{jj} [GeV]'  ,                   'ytitle':'Events', 'rebin':5,  'ymin':1.0,'logy':False, 'LtoRCut':0}, #, 'xmax':1500
        'jjg_mass'    : {'xtitle':'#it{m}_{jj#gamma} [GeV]'  ,'ytitle':'Events / 500 GeV', 'rebin':5,  'ymin':1.0,'logy':True, 'LtoRCut':0},
        'j1g_dR'    : {'xtitle':'#DeltaR(#gamma,Lead Jet)'  ,'ytitle':'Events', 'rebin':2,  'ymin':1.0,'logy':True, 'LtoRCut':0},
        'j2g_dR'    : {'xtitle':'#DeltaR(#gamma,SubLead Jet)'  ,'ytitle':'Events', 'rebin':2,  'ymin':1.0,'logy':True, 'LtoRCut':0},
        'j3g_dR'    : {'xtitle':'#DeltaR(#gamma,Third Jet)'  ,'ytitle':'Events', 'rebin':2,  'ymin':1.0,'logy':True, 'LtoRCut':0},
        'jj_mass_variableBin'    : {'xtitle':'#it{m}_{jj} [GeV]'  ,        'xmin':200.0, 'xmax':5000.0,    'ymin':0.1,      'ytitle':'Events / 500 GeV', 'rebin':0, 'logy':False, 'LtoRCut':2}, # #for Z  # for W 'ymin':50.1,'ymax':30000,##'xmin':800.0, 'xmax':5000.0, 'ymin':50.1,'ymax':30000, 'ymin':50.1,'ymax':20000,
        'jj_mass_variableBinGam'    : {'xtitle':'#it{m}_{jj} [GeV]'  ,        'xmin':250.0,     'ymin':0.1,      'ytitle':'Events / 500 GeV', 'rebin':0, 'logy':False, 'LtoRCut':2}, # #for Z  # for W 'ymin':50.1,'ymax':30000,##'xmin':800.0, 'xmax':5000.0, 'ymin':50.1,'ymax':30000, 'ymin':50.1,'ymax':20000,         'xmax':3500.0,
        'tmva_variableBin'    : {'xtitle':'ANN Output'  ,                   'ytitle':'Events', 'rebin':0,  'ymin':0.01,'logy':False, 'LtoRCut':2},
        'tmva_variableBin11'    : {'xtitle':'ANN Output'  ,                   'ytitle':'Events', 'rebin':0,  'ymin':10.01,'logy':True, 'LtoRCut':2},
        'tmva_wmj_variableBin'    : {'xtitle':'ANN Output'  ,                   'ytitle':'Events', 'rebin':0,  'ymin':10.01,'logy':True, 'LtoRCut':2},
        'tmva_wmj_variableBin11'    : {'xtitle':'ANN Output'  ,                   'ytitle':'Events', 'rebin':0,  'ymin':10.01,'logy':True, 'LtoRCut':2},                        
        'jj_deta' : {'xtitle':'#Delta #it{#eta}_{jj}'  ,               'ytitle':'Events', 'rebin':2,  'ymin':0.001, 'LtoRCut':0},
        'jj_deta_signed' : {'xtitle':'Signed #Delta #it{#eta}_{jj}'  ,               'ytitle':'Events', 'rebin':0,  'ymin':0.001, 'LtoRCut':0},
        'jj_deta_diff' : {'xtitle':'|#it{#eta}_{j2}| - |#it{#eta}_{j1}|'  ,'ytitle':'Events', 'rebin':0,  'ymin':0.001, 'LtoRCut':0},
        'jj_deta_abs' : {'xtitle':'|#it{#eta}_{j2}| - |#it{#eta}_{j1}|/#Delta#it{#eta}_{jj}'  ,'ytitle':'Events', 'rebin':0,  'ymin':0.001, 'LtoRCut':0},                
        'ptll'   : {'xtitle':'#it{p}_{T,ll} [GeV]',                   'ytitle':'Events / (25 GeV)', 'rebin':5,  'ymin':0.0},
        'ptllg'   : {'xtitle':'#it{p}_{T,ll#gamma} [GeV]',                   'ytitle':'Events / (25 GeV)', 'rebin':5,  'ymin':0.0},
        'mt'     : {'xtitle':'#it{m}_{T} [GeV]'   ,         'ytitle':'Events / (10 GeV)', 'rebin':4,  'ymin':0.01,'logy':False},
        'mtgammet'     : {'xtitle':'#it{m}_{T} (#gamma,MET) [GeV]'   ,         'ytitle':'Events / (10 GeV)', 'rebin':1,  'ymin':0.01,'logy':False,'xmax':250.0},
        'mtgammet_variableBinGam'     : {'xtitle':'#it{m}_{T} (#gamma,MET) [GeV]'   ,         'ytitle':'Events / (30 GeV)', 'rebin':1,  'ymin':0.01,'logy':False},
        'mtlepgammet'     : {'xtitle':'#it{m}_{T} (Lead Lep+#gamma,MET) [GeV]'   ,'ytitle':'Events / (10 GeV)', 'rebin':10,  'ymin':0.01,'logy':False},
        'met_significance'     : {'xtitle':'#it{S}_{MET} [GeV^{1/2}]'   ,         'ytitle':'Events / GeV^{1/2}', 'rebin':2,  'ymin':0.1,'logy':True},
        'metsig_variableBin'     : {'xtitle':'#it{S}_{MET} [GeV^{1/2}]'   ,         'ytitle':'Events / GeV^{1/2}', 'rebin':1,  'ymin':2,'logy':True},
        'metsig_tst'     : {'xtitle':'#it{S}_{MET}^{TST} [GeV^{1/2}]'   ,         'ytitle':'Events', 'rebin':2,  'ymin':0.01,'logy':True},
        'alljet_metsig'     : {'xtitle':'#it{S}_{MET} (all jets) [GeV^{1/2}]'   ,         'ytitle':'Events', 'rebin':10,  'ymin':0.1,'logy':True},
    'met_cst_jet'     : {'xtitle':'#it{E}_{T}^{jet,no-JVT} [GeV]'   ,         'ytitle':'Events', 'rebin':1,  'ymin':5.1},
    'met_cst_tst_sub'     : {'xtitle':'#it{E}_{T}^{jet,no-JVT}-#it{E}_{T}^{miss} [GeV]'   ,         'ytitle':'Events',   'ymin':5.1},
    'met_cst_tst_ratio'     : {'xtitle':'|1-#it{E}_{T}^{jet,no-JVT}/#it{E}_{T}^{miss}|'   ,         'ytitle':'Events', 'ymin':5.1},
    'met_truth_et'     : {'xtitle':'Truth MET [GeV]'   ,         'ytitle':'Events',   'ymin':0.1,'logy':True,'LtoRCut':0,'xmax':500.0,'ymax':1.0e4},
    'met_tighter_tst_et'     : {'xtitle':'Tighter MET [GeV]'   ,         'ytitle':'Events', 'rebin':10,  'ymin':0.1},
    'met_tenacious_tst_et'     : {'xtitle':'Tenacious MET [GeV]'   ,         'ytitle':'Events',  'rebin':5, 'ymin':0.1},
    'met_tenacious_tst_nolep_et'     : {'xtitle':'Tenacious MET (without leptons) [GeV]'   ,         'ytitle':'Events',  'rebin':10, 'ymin':0.1},    
    'FilterMet'     : {'xtitle':'Filter MET [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'truth_jj_mass'     : {'xtitle':'Truth #it{m}_{jj} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'truth_jj_deta'     : {'xtitle':'Truth #Delta#it{#eta}_{jj}'   ,         'ytitle':'Events',   'ymin':0.1},
    'truth_jj_dphi'     : {'xtitle':'Truth #Delta#it{#phi}_{jj}'   ,         'ytitle':'Events / 0.2 rad',   'ymin':0.1},
    'truth_j1_pt'     : {'xtitle':'Truth lead Jet #it{p}_{T} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'truth_j2_pt'     : {'xtitle':'Truth lead Jet #it{p}_{T} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'SherpaVTruthPt'     : {'xtitle':'Sherpa #it{p}_{T} V [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},                
    'truthJet1Pt'     : {'xtitle':'Truth sub-lead Jet #it{p}_{T} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'nTruthJetMatch'     : {'xtitle':'Number of Truth Matched Jets'   ,         'ytitle':'Events',   'ymin':0.1},
    'n_baseel'     : {'xtitle':'Number of Base Electrons'   ,         'ytitle':'Events',   'ymin':0.1},
    'n_tau'     : {'xtitle':'Number of Taus'   ,         'ytitle':'Events',   'ymin':0.1},
    'n_basemu'     : {'xtitle':'Number of Base Muons'   ,         'ytitle':'Events',   'ymin':0.1},
    'n_truth_tau'     : {'xtitle':'Number of Truth taus'   ,         'ytitle':'Events',   'ymin':0.1},
    'met_tst_j1_dphi'     : {'xtitle':'#Delta#it{#phi}(j1,MET)'   ,         'ytitle':'Events',   'ymin':0.1},
    'met_tst_j2_dphi'     : {'xtitle':'#Delta#it{#phi}(j2,MET)'   ,         'ytitle':'Events',   'ymin':0.1},
    'ptvarcone20'     : {'xtitle':'ptvarcone20/#it{p}_{T}'   ,         'ytitle':'Events',   'ymin':0.1},
    'baselep_ptvarcone_0'     : {'xtitle':'ptvarcone20/#it{p}_{T}'   ,         'ytitle':'Events'},
    'ptvarcone30'     : {'xtitle':'ptvarcone30/#it{p}_{T}'   ,         'ytitle':'Events',   'ymin':0.1},
    'topoetcone20'     : {'xtitle':'topoetcone20/#it{p}_{T}'   ,         'ytitle':'Events',   'ymin':0.1},

    'mj34'     : {'xtitle':'#it{m}_{j3,j4} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'max_j_eta'     : {'xtitle':'max(#it{#eta}_{j1},#it{#eta}_{j2})'   ,         'ytitle':'Events',   'ymin':0.1},
    'dRj1'     : {'xtitle':'#DeltaR(j1,j3)'   ,         'ytitle':'Events',   'ymin':0.1},
    'dRj2'     : {'xtitle':'#DeltaR(j2,j3)'   ,         'ytitle':'Events',   'ymin':0.1},
    'dRj12'     : {'xtitle':'#DeltaR(j1,j2)'   ,         'ytitle':'Events',   'ymin':0.1},    
    'dRj13'     : {'xtitle':'#DeltaR(j1,j3)'   ,         'ytitle':'Events',   'ymin':0.1},    
    'dRj23'     : {'xtitle':'#DeltaR(j2,j3)'   ,         'ytitle':'Events',   'ymin':0.1},
    'dRj34'     : {'xtitle':'#DeltaR(j3,j4)'   ,         'ytitle':'Events',   'ymin':0.1},        
    'dPhij13'     : {'xtitle':'#Delta#phi(j1,j3)'   ,         'ytitle':'Events',   'ymin':0.1},        
    'dPhij23'     : {'xtitle':'#Delta#phi(j2,j3)'   ,         'ytitle':'Events',   'ymin':0.1},        
    'dPhij34'     : {'xtitle':'#Delta#phi(j3,j4)'   ,         'ytitle':'Events',   'ymin':0.1},        
    'rPTj31'     : {'xtitle':'#it{p}_{T}^{j3}/#it{p}_{T}^{j1}'   ,         'ytitle':'Events',   'ymin':0.1},
    'rPTj21'     : {'xtitle':'#it{p}_{T}^{j2}/#it{p}_{T}^{j1}'   ,         'ytitle':'Events',   'ymin':0.1},
    'rPTj32'     : {'xtitle':'#it{p}_{T}^{j3}/#it{p}_{T}^{j2}'   ,         'ytitle':'Events',   'ymin':0.1},
    'rPTj43'     : {'xtitle':'#it{p}_{T}^{j4}/#it{p}_{T}^{j3}'   ,         'ytitle':'Events',   'ymin':0.1},
    'minDR'     : {'xtitle':'min #DeltaR(j1/j2,j3)'   ,         'ytitle':'Events',   'ymin':0.1},
    'gamLepDR' : {'xtitle':'min #DeltaR(lep,#gamma)'   ,         'ytitle':'Events',   'ymin':0.1},
    'gamJetDR' : {'xtitle':'min #DeltaR(jet,#gamma)'   ,         'ytitle':'Events',   'ymin':0.1},
    'mj1'     : {'xtitle':'#it{m}_{j1,j3} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'mj2'     : {'xtitle':'#it{m}_{j2,j3} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'minDRmj2'     : {'xtitle':'minDR #it{m}_{j1/j2,j3} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'min_mj3'     : {'xtitle':'min #it{m}_{j1/j2,j3} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'min_mj3_over_mjj'     : {'xtitle':'min #it{m}_{j1/j2,j3} / #it{m}_{j1,j2}'   ,         'ytitle':'Events',   'ymin':0.1},
    'centrality'     : {'xtitle':'j3 Centrality',         'ytitle':'Events',   'ymin':0.1,'rebin':1},
    'phcentrality'     : {'xtitle':'#it{#gamma} Centrality'   ,         'ytitle':'Events',   'ymin':0.1,'rebin':5},
    'phPt'     : {'xtitle':'#it{#gamma} #it{p}_{T} [GeV]'   ,         'ytitle':'Events / 10 GeV',  'rebin':2,'logy':False, 'ymin':0.01},
    'phEta'     : {'xtitle':'#it{#gamma} #it{#eta}'   ,         'ytitle':'Events', 'rebin':2,  'ymin':0.1},
    'met_tst_ph_dphi'     : {'xtitle':'#Delta#it{#phi}(#gamma,MET)'   ,         'ytitle':'Events',  'rebin':2,  'ymin':0.1},
    'met_tst_nolep_ph_dphi'     : {'xtitle':'#Delta#it{#phi}(#gamma,MET(without leptons))'   ,         'ytitle':'Events',   'ymin':0.1},
    'Mtt'     : {'xtitle':'#it{m}_{#tau#tau} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1},
    'minDRLep'     : {'xtitle':'min #DeltaR(j,lep)'   ,         'ytitle':'Events',   'ymin':0.1},
    'j3Pt'     : {'xtitle':'j3 #it{p}_{T} [GeV]'   ,         'ytitle':'Events',   'ymin':0.1, 'LtoRCut':0},
    'j3Eta'     : {'xtitle':'j3 #it{#eta}'   ,         'ytitle':'Events',   'ymin':0.1},
    'j3Jvt'     : {'xtitle':'j3 Jvt'   ,         'ytitle':'Events',   'ymin':0.1},
    'j3FJvt'     : {'xtitle':'j3 f-Jvt'   ,         'ytitle':'Events',   'ymin':0.1},
    'jetPt3'     : {'xtitle':'j3 #it{p}_{T} [GeV]'   ,         'ytitle':'Events / 10 GeV',   'ymin':0.1, 'LtoRCut':False},
    'avgCentrality'     : {'xtitle':'Average jet Centrality'   ,         'ytitle':'Events',   'ymin':0.1, 'LtoRCut':True},
    'maxCentrality'     : {'xtitle':'Max jet Centrality'   ,         'ytitle':'Events',   'ymin':0.1, 'LtoRCut':True,'rebin':5},
    'avgmj3_over_mjj'     : {'xtitle':'Average min #it{m}_{j1/j2,j3} / #it{m}_{j1,j2}'   ,         'ytitle':'Events',   'ymin':0.1, 'LtoRCut':True},
    'maxmj3_over_mjj'     : {'xtitle':'Max min #it{m}_{j1/j2,j3} / #it{m}_{j1,j2}'   ,         'ytitle':'Events',   'ymin':0.1, 'LtoRCut':True},
    'max_j3_dr'     : {'xtitle':'Max min #Delta#it{R}_{j1/j2,j3}'   ,'ytitle':'Events',   'ymin':0.1, 'LtoRCut':False},
    'met_tst_j3_dphi'     : {'xtitle':'Max #Delta#it{#phi}_{MET,j3}'   ,'ytitle':'Events',   'ymin':0.1, 'LtoRCut':False,'rebin':5},
    'met_tst_nolep_j3_dphi'     : {'xtitle':'Max #Delta#it{#phi}_{MET,j3}'   ,'ytitle':'Events',   'ymin':0.1, 'LtoRCut':False,'rebin':5},
    'ph_pointing_z'     : {'xtitle':'Photon pointing - vertex z-position [mm]'   ,'ytitle':'Events',   'ymin':0.1, 'LtoRCut':False,'rebin':5},
        }

    try:
        return labels[hist]
    except KeyError:
        log.warning('getHistPars - unknown histogram: %s' %hist)
        return labels

#-------------------------------------------------------------------------
def getLabelSortKey(sample):

    if   sample == 'top2': return 1
    elif sample == 'data': return 0    # 11
    elif sample == 'wzzz': return 2
    elif sample == 'tth': return -5        
    elif sample == 'vbfg': return -5        
    elif sample == 'wz': return 2
    elif sample == 'zz': return 4
    elif sample == 'smww': return 1 # was 3
    elif sample == 'top1': return 4
    elif sample == 'tall': return 20
    elif sample == 'mqcd': return 5
    elif sample == 'dqcd': return 5
    elif sample == 'vvv': return 6
    elif sample == 'zldy': return 7
    elif sample == 'zjet': return 18
    elif sample == 'qflip': return 3
    elif sample == 'zjhf': return 18
    elif sample == 'zvbf': return 18
    elif sample == 'zall': return 18
    elif sample == 'zjll': return 18
    elif sample == 'zjtt': return 7
    elif sample == 'wjet': return 6
    elif sample == 'wjdt': return 1
    elif sample == 'dqcd': return 18
    elif sample == 'susy': return 18
    elif sample == 'wjdte': return 16
    elif sample == 'wjdtm': return 17
    elif sample == 'zqcd': return -8
    elif sample == 'zqcdMad': return 8
    elif sample == 'hggf': return 9
    elif sample == 'hvbf': return 10
    #elif sample == 'data': return 11
    elif sample == 'bkgs': return 12
    elif sample == 'zewk': return -7
    elif sample == 'ttg': return 13
    elif sample == 'zgamewk': return 15        
    elif sample == 'wgamewk': return 15
    elif sample == 'zgam': return 13
    elif sample == 'wgam': return 13        
    elif sample == 'pho': return 13
    elif sample == 'wqcd': return -10
    elif sample == 'wqcdMad': return 14
    elif sample == 'wewk': return -9
    elif sample == 'wdpi': return 16
    elif sample == 'wgas': return 17
    elif sample == 'vvv': return 6
    elif sample == 'ttv': return 7
    elif sample == 'higgs': return 20
    elif sample == 'whww': return 20        
    elif sample == 'jpsi': return 21
    elif sample == 'upsl': return 22
    elif sample == 'efakeph': return 22
    elif sample == 'jfakeph': return 22
    elif sample == 'gamd': return 23

    log.warning('getSampleSortKey - unknown key: %s' %sample)
    return 100

#-------------------------------------------------------------------------
def getSampleSortKey(sample):

    if   sample == 'smww': return 1
    elif sample == 'zqcd': return 8
    elif sample == 'zqcdMad': return -8
    elif sample == 'tth': return -4.5
    elif sample == 'vbfg': return -4.5
    elif sample == 'zewk': return 7        
    elif sample == 'wqcd': return 10
    elif sample == 'wqcdMad': return -2
    elif sample == 'wewk': return 9
    elif sample == 'top2': return 4
    elif sample == 'top1': return 5
    elif sample == 'tall': return -5
    elif sample == 'mqcd': return 5
    elif sample == 'dqcd': return -5
    elif sample == 'susy': return -5
    elif sample == 'vvv': return 6
    elif sample == 'zldy': return 7
    elif sample == 'higgs': return 8
    elif sample == 'whww': return 8        
    elif sample == 'hggf': return 8
    elif sample == 'hvbf': return 9
    elif sample == 'data': return -10
    elif sample == 'bkgs': return 11
    elif sample == 'ttg': return 13        
    elif sample == 'zgam': return 13        
    elif sample == 'wgam': return 13
    elif sample == 'zgamewk': return 15
    elif sample == 'wgamewk': return 15
    elif sample == 'pho': return 13
    elif sample == 'efakeph': return 13
    elif sample == 'jfakeph': return 13        
    elif sample == 'gamd': return 14        

    log.warning('getLabelSortKey - unknown key: %s' %sample)
    return 100

#-------------------------------------------------------------------------
def getSampleLabel(sample):

    if options.hscale != None:
        hlabel = '%s #times %d' %(options.hmass, options.hscale)
    else:
        hlabel = options.hmass

    labels = {
        'smww': '#it{WW/W#gamma}',
        'zjet': '#it{Z}+jets',
        'qflip': 'Charge Flip',
        'zqcd': '#it{Z} strong',
        'zqcdMad': '#it{Z} strong',
        'tth': 'Fake-#it{e}',
        'vbfg': 'Fake-#it{e}',
        'zewk': '#it{Z} EWK',
        'mqcd': 'Multijet',
        'dqcd': 'Multijet',
        'susy': '%0.2f#timesVBF_150_149p8' %(options.hscale),
        'wqcd': '#it{W} strong',
        'wqcdMad': '#it{W} strong',
        'wewk': '#it{W} EWK',
        'top1': 'Single Top',
        'top2': 'Top', #'t#bar{t}',
        'tall': 'Other',#'Top+#it{VV}/#it{VVV}',
        'vvv': '#it{VV}/#it{VVV}',
        'zldy': '#it{Z} low m.',
        'wzzz': '#it{ZV}',#'WZ/ZZ',
        'wz': '#it{WZ}',
        'zz': '#it{ZZ}',
        'wgam': '#it{W#gamma} strong',
        'wgas': '#it{W#gamma*}',
        'zgas': '#it{Z#gamma*}',
        'zgam': '#it{Z#gamma} strong',
        'efakeph': '#it{e}#rightarrow#gamma',
        'jfakeph': 'jet#rightarrow#gamma',
        'zgamewk': '#it{Z#gamma} EWK',
        'wgamewk': '#it{W#gamma} EWK',
        'ttg': '#it{t#bar{t}#gamma}',
        'pho': '#it{#gamma}+j',
        'htau':  '%s #it{H}#rightarrow#tau#tau'%options.hmass,
        'hggf':  'ggF Higgs',
        'whww':  'VBFH2000',        
        #'higgs':  '#it{h}(#it{B}_{inv} = 0.13)',
        #'hvbf':  '#it{h}(#it{B}_{inv} = 0.13)',
        'higgs':  '#it{H} (#it{B}_{inv} = %0.2f)' %options.hscale,
        'gamd':  '#it{H} (#it{B}_{#gamma_{dark}} = %0.2f)' %options.hscalealt,        
        #'higgs':  '#it{H} (#it{B}_{inv} = 1.00)' ,
        'hvbf':  '#it{H} (#it{B}_{inv} = %0.2f)' %options.hscale,
        'ttv' : 't#bar{t}V+tV',
        'data': 'Data',
        'bkgs': 'Total SM',
        }

    try:
        return labels[sample]
    except KeyError:
        log.error('getSampleLabel - unknown sample: %s' %sample)
        sys.exit(1)

#-------------------------------------------------------------------------
def getColor(color_index):

    color_vec=[2, 3, 4, 5, 6,
               ROOT.kBlue   -9,
               ROOT.kGreen  -3,
               ROOT.kCyan   -9,
               ROOT.kYellow +2,
               ROOT.kYellow +1,
               ROOT.kMagenta-3,
               ROOT.kOrange,
               ROOT.kOrange-3,
               ]

    if len(color_vec)>color_index:
        return color_vec[color_index]
    return color_index

#-------------------------------------------------------------------------
def getStyle(sample):
    #
    # Read mini dilep ntuple
    #
    #color_zewk = ROOT.kBlue   -9
    #color_zqcd = ROOT.kGreen  -3
    #color_wqcd = ROOT.kGreen  -7
    #color_wewk = ROOT.kCyan   -9
    # version 2
    #color_zewk = ROOT.kCyan   -9
    #color_zqcd = ROOT.kBlue-9
    #color_wqcd = ROOT.kGreen  -3
    #color_wewk = ROOT.kGreen  -7
    #color_tall = ROOT.kMagenta-9 #ROOT.kYellow +1 #ROOT.kRed+1
    #color_wdpi = ROOT.kGray+1#ROOT.kOrange-5
    # version cool
    color_fake = ROOT.kViolet-4
    color_zewk = ROOT.kSpring+8
    color_zqcd = ROOT.kGreen-2
    #color_wqcd = ROOT.kCyan-3
    #color_wewk = ROOT.kTeal
    color_wqcd = ROOT.kOrange+2
    color_wewk = ROOT.kOrange+1
    color_tall = ROOT.kBlue-6
    color_wdpi = ROOT.kMagenta-10
    color_top1 = ROOT.kYellow +2
    color_top2 = ROOT.kYellow +1
    color_wzzz = ROOT.kMagenta-3
    color_wz = ROOT.kTeal-8 #ROOT.kMagenta-3
    color_zz = ROOT.kAzure-4 #ROOT.kMagenta-3
    color_vvv = ROOT.kOrange
    color_zldy = ROOT.kOrange-3
    color_wgam = ROOT.kOrange
    color_zgam = ROOT.kOrange-3
    color_efakeph = ROOT.kGreen-2
    color_jfakeph = ROOT.kGreen-3
    color_wgamewk = ROOT.kOrange-5
    color_zgamewk = ROOT.kOrange-6
    color_ttg = ROOT.kBlue   -9
    color_pho = ROOT.kGreen -3
    color_wgas = ROOT.kOrange-7
    color_zgas = ROOT.kOrange-7
    color_higgs = ROOT.kViolet-9 #ROOT.kRed    +0
    color_hvbf = ROOT.kRed+1 #ROOT.kRed    +0
    color_gamd = ROOT.kRed+2 #ROOT.kRed    +0
    color_hggf = ROOT.kRed+1 #ROOT.kRed    +0
    color_higgsall = ROOT.kRed+1 #ROOT.kRed    +0
    color_bkgs = ROOT.kBlue   +1
    color_data = ROOT.kBlack

    styles = {
        'vbfg':{'color':color_fake, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'tth':{'color':color_fake, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'zewk':{'color':color_zewk, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'zqcd':{'color':color_zqcd, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'zqcdMad':{'color':color_zqcd, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'wqcd':{'color':color_wqcd, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'wqcdMad':{'color':color_wqcd, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'wewk':{'color':color_wewk, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'top1':{'color':color_top1, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'top2':{'color':color_top2, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'mqcd':{'color':color_wdpi, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'dqcd':{'color':color_wdpi, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'tall':{'color':color_tall, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'pho':{'color':color_pho, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},        
        'ttg':{'color':color_ttg, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},        
        'zgam':{'color':color_zgam, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'efakeph':{'color':color_efakeph, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'jfakeph':{'color':color_jfakeph, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},        
        'wgam':{'color':color_wgam, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'zgamewk':{'color':color_zgamewk, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},        
        'wgamewk':{'color':color_wgamewk, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'vvv':{'color':color_vvv, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'zldy':{'color':color_zldy, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'higgs':{'color':color_higgsall, 'fill_style':0, 'marker_style': 0, 'line_width':5,'line_style':2, 'leg_opt':'f'},
        'hggf':{'color':color_hggf, 'fill_style':0, 'marker_style': 0, 'line_width':5, 'leg_opt':'f'},
        'susy':{'color':color_gamd, 'fill_style':0, 'marker_style': 0, 'line_width':5,'line_style':3, 'leg_opt':'f'},
        'whww':{'color':color_gamd, 'fill_style':0, 'marker_style': 0, 'line_width':5,'line_style':3, 'leg_opt':'f'},        
        'hvbf':{'color':color_hvbf, 'fill_style':0,    'marker_style': 0, 'line_width':5, 'leg_opt':'f'},
        'gamd':{'color':color_gamd, 'fill_style':0,    'marker_style': 0, 'line_width':5, 'leg_opt':'f'},        
        'data':{'color':color_data, 'fill_style':0,    'marker_style':20, 'line_width':0, 'leg_opt':'ple'},
        'bkgs':{'color':color_bkgs, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        }

    if options.stack_signal:
        styles[options.signal]={'color':color_higgs, 'fill_style':3144,    'marker_style': 0, 'line_width':0, 'leg_opt':'f'}

    try:
        return styles[sample]
    except KeyError:
        log.error('getLabel - unknown sample: %s' %sample)
        sys.exit(1)

#-------------------------------------------------------------------------
def updateCanvas(can, name=None, leg=None, option = '', data_hist=None, bkg_sum_hist=None):

    if not can:
        sys.exit(0)

    can.Modified()
    can.Update()

    plist = can.GetPad(0).GetListOfPrimitives()

    hists = []

    stath = 0.25
    staty = 1.0
    statw = 0.20
    statx = 0.80

    for p in plist:
        try:
            if not p.InheritsFrom('TH1'):
                continue
            p.GetYaxis().SetTitleSize(0.055)
            #p.GetYaxis().SetTitleOffset(0.1)
            hists.append(p)
            stats = p.FindObject('stats')

            if stats:
                stats.SetTextColor(p.GetLineColor())
                stats.SetY1NDC(staty-stath)
                stats.SetY2NDC(staty)
                stats.SetX2NDC(statx+statw)
                stats.SetX1NDC(statx)
                staty = staty - stath
        except:
            print 'Failed'

    can.Modified()
    can.Update()

    if options.wait:
        can.WaitPrimitive()

    if not can:
        sys.exit(0)

    if options.save and name != None:
        if options.do_logy:
            name+='_logy'
        if options.pref != None:
            name = '%s_%s' %(options.pref, name)
        if options.preliminary:
            name+='_prelim'
        if options.outdir != None:
            if not os.path.exists(options.outdir): os.system('mkdir %s' %(options.outdir))
            name = '%s/%s' %(options.outdir.rstrip(), name)

        can.Print('%s.png' %name, 'png')

        if options.do_eps:
            can.Print('%s.eps' %name, 'eps')

        # Support generating .C macro to remake plot.
        if options.do_c:
            can.SaveAs('%s.C' % name)

        if options.do_pdf:
            can.Print('%s.pdf' %name, 'pdf')

        if options.do_root:
            #outfile  = ROOT.TFile("hists_"+name+".root", "RECREATE")
            outfile  = ROOT.TFile('%s.root' %name, "RECREATE")
            can.Write()
            if data_hist:
                data_hist.hist.SetDirectory(outfile)
                data_hist.hist.SetName("data_"+data_hist.hist.GetName())
                data_hist.hist.Write()
            if bkg_sum_hist:
                bkg_sum_hist.SetDirectory(outfile)
                bkg_sum_hist.SetName("totbkg_"+bkg_sum_hist.GetName())
                bkg_sum_hist.Write()
            outfile.Close()
            print "file "+str(outfile)+" has been created"


#-------------------------------------------------------------------------
def rescaleFirstBin(hist, scale):

    if not hist or not (scale > 0.0) or hist.GetNbinsX() < 2:
        return

    val = hist.GetBinContent(1)
    err = hist.GetBinError  (1)

    hist.SetBinContent(1, val*scale)
    hist.SetBinError  (1, err*scale)

    xl = hist.GetXaxis().GetBinCenter (1)- 0.3*hist.GetXaxis().GetBinWidth(1)
    yl = hist.GetBinContent(1)+ 5.0*hist.GetBinError(1)

    #c = ROOT.TLatex(0.15, 0.1, '#times %.1f' %scale)
    c = ROOT.TLatex(xl, yl, '#times %.1f' %scale)
    c.SetNDC(False)
    c.SetTextFont(42)
    c.SetTextSize(0.05)
    c.SetTextAlign(12)
    c.SetTextColor(ROOT.kBlack)

    return c

#-------------------------------------------------------------------------
class HistEntry:
    """HistEntry - one histogram in a stacked plot"""

    def __init__(self, hist, sample, hname, nf_map, ZCR=None, WCR=None):

        self.sample   = sample
        self.hname    = hname
        self.hist     = hist.Clone()
        self.leg_opt  = 'l'
        self.leg_text = getSampleLabel(sample)
        self.text1st  = None
        self.nf_map   = nf_map

        self.hist.SetStats    (False)
        self.hist.SetDirectory(0)

        #
        # Add overflow
        #
        if not options.no_underflow:
            self.hist.SetBinContent(1,self.hist.GetBinContent(0)+self.hist.GetBinContent(1))
            self.hist.SetBinError(1,math.sqrt(self.hist.GetBinError(0)**2+self.hist.GetBinError(1)**2))
            self.hist.SetBinContent(0,0)
            self.hist.SetBinError(0,0)
            last_bin=self.hist.GetNbinsX()
            # find last bin if option is set
            if 'xmax' in getHistPars(self.hname):
                for mbin in range(0,self.hist.GetNbinsX()+1):
                    if self.hist.GetXaxis().GetBinUpEdge(mbin)>=getHistPars(self.hname)['xmax']:
                        last_bin=mbin
                        break
            #print 'last_bin: ',last_bin,' ',self.hist.GetNbinsX()
            my_err = ROOT.Double(0)
            my_last_bin_val = self.hist.IntegralAndError(last_bin,self.hist.GetNbinsX()+5, my_err)
            self.hist.SetBinContent(last_bin,my_last_bin_val)
            self.hist.SetBinError(last_bin,my_err)
            for mbin in range(last_bin+1,self.hist.GetNbinsX()+2):
                self.hist.SetBinContent(mbin,0.0)
                self.hist.SetBinError(mbin,0.0)
                
        if self.sample in self.nf_map:
            self.hist.Scale(self.nf_map[self.sample])
            log.info('Scaling Sample %s by %s ' %(self.sample,self.nf_map[self.sample]))
        self.UpdateStyle(sample)

        # apply the Normalization for the ZCR and WCR if requested.
        madgraph=''
        if options.madgraph:
            madgraph='Mad'
        if ZCR and (sample in ['zqcd'+madgraph,'zewk']) and options.normalizeBkg:
            for i in range(0,self.hist.GetNbinsX()+1):
                znf,znferr = ZCR.GetNF(['zqcd'+madgraph,'zewk'],i)
                self.hist.SetBinContent(i,znf*self.hist.GetBinContent(i))
                self.hist.SetBinError(i,math.sqrt((znf*self.hist.GetBinError(i))**2+(znferr*self.hist.GetBinContent(i))**2))
                
        if WCR and (sample in ['zqcd'+madgraph,'zewk']) and options.normalizeWBkg:
            for i in range(0,self.hist.GetNbinsX()+1):
                znf,znferr = WCR.GetNF(['wqcd'+madgraph,'wewk'],i)
                self.hist.SetBinContent(i,znf*self.hist.GetBinContent(i))
                #self.hist.SetBinError(i,znf*self.hist.GetBinError(i))
                self.hist.SetBinError(i,math.sqrt((znf*self.hist.GetBinError(i))**2+(znferr*self.hist.GetBinContent(i))**2))
        if WCR and (sample in ['wqcd'+madgraph,'wewk']) and (options.normalizeBkg or options.normalizeWBkg):
            for i in range(1,self.hist.GetNbinsX()+1):
                wnf,wnferr = WCR.GetNF(['wqcd'+madgraph,'wewk'],i)
                self.hist.SetBinContent(i,wnf*self.hist.GetBinContent(i))
                #self.hist.SetBinError(i,wnf*self.hist.GetBinError(i))
                self.hist.SetBinError(i,math.sqrt((wnf*self.hist.GetBinError(i))**2+(wnferr*self.hist.GetBinContent(i))**2))

    def UpdateStyle(self, sample):

        self.sample   = sample
        self.leg_text = getSampleLabel(sample)

        style = getStyle   (sample)
        hpars = getHistPars(self.hname)

        self.logy = 'logy' in hpars and hpars['logy']
        if options.do_logy:
            self.logy = options.do_logy
        if 'xtitle' in hpars:
            self.hist.GetXaxis().SetTitle(hpars['xtitle'])
        if 'ytitle' in hpars:
            self.hist.GetYaxis().SetTitle(hpars['ytitle'])
        if 'color' in style:
            self.hist.SetLineColor(style['color'])
            self.leg_opt = 'f'

            if 'fill_style' in style and style['fill_style'] > 0:
                self.hist.SetLineColor(ROOT.kBlack)
                self.hist.SetLineWidth(1)
                self.hist.SetFillColor(style['color'])
                self.hist.SetLineColor(style['color'])
                self.hist.SetFillStyle(style['fill_style'])
                self.leg_opt = 'f'

            elif 'marker_style' in style and style['marker_style'] > 0:
                self.hist.SetMarkerColor(style['color'])
                self.hist.SetMarkerStyle(style['marker_style'])
                self.leg_opt = 'p'

        if 'line_width' in style and style['line_width'] > 0:
            self.hist.SetLineWidth(style['line_width'])
        if 'line_style' in style and style['line_style'] > 0:
            self.hist.SetLineStyle(style['line_style'])

        if 'leg_opt' in style:
            self.leg_opt = style['leg_opt']

        if 'rebin' in hpars and hpars['rebin'] > 1:
            self.hist.Rebin(hpars['rebin'])
        if 'scale1st' in hpars:
            self.text1st = rescaleFirstBin(self.hist, hpars['scale1st'])

    def DrawHist(self, opt=None, leg=None, my_signal=False):
        if self.hist == None:
            return

        if type(opt) == type(''):
            if options.draw_norm: self.hist.DrawNormalized(opt)
            else:                 self.hist.Draw(opt)
        if leg != None:
            if my_signal:
                leg.AddEntry(self.hist, self.leg_text,"l")
            else:
                leg.AddEntry(self.hist, self.leg_text, self.leg_opt)

#-------------------------------------------------------------------------
class SystHists:
    """ Collection of systematics histograms for all bakgrounds"""

    def __init__(self):
        pass

#-------------------------------------------------------------------------
def getSystSumSortKey(value):
    return math.fabs(value[1]-value[2])

#-------------------------------------------------------------------------
class DrawStack:
    """DrawStack - a set of histograms for one stacked plot"""

    def __init__(self, name, file, sign, data, bkgs, nf_map, extract_sig, selkey=options.selkey, extrasignal=None):

        self.name   = name
        self.selkey = selkey
        self.algkey = options.algkey
        self.nf_map = nf_map
        self.file_pointer = file
        self.zcr_stack = None
        self.wcr_stack = None
        
        if ((options.blind or options.normalizeBkg or options.normalizeWBkg) and self.selkey.count('pass_sr') and self.selkey.count('_nn_')): #and self.selkey=='pass_sr_allmjj_nn_Nominal':
            replace_sr_name = self.selkey[self.selkey.find('pass_sr_')+len('pass_sr_'): self.selkey.find('_nn_')]
            zcr_name=copy.copy(name)
            if zcr_name.count('_tst_et') and not zcr_name.count('_nolep') and not zcr_name.count('soft'):
                zcr_name = zcr_name.replace('_tst_et','_tst_nolep_et')
            systName = self.selkey[self.selkey.find('_nn_')+4:]
            self.zcr_stack = DrawStack(zcr_name, file, sign, data, bkgs, nf_map, extract_sig, selkey='pass_zcr_'+replace_sr_name+'_ll_'+systName)
            self.wcr_stack = DrawStack(zcr_name, file, sign, data, bkgs, nf_map, extract_sig, selkey='pass_wcr_'+replace_sr_name+'_l_'+systName)            
            
        self.sign = self.ReadSample(file, sign)
        self.signextra=None
        if extrasignal:
            self.signextra = self.ReadSample(file, extrasignal)        
        if options.hscale!=None:
            self.sign.hist.Scale(float(options.hscale))
            if extrasignal:
                self.signextra.hist.Scale(float(options.hscalealt))                
        self.data = self.ReadSample(file, data)
        self.abkg = None
        self.bkgs = {}
        self.extract_sig = {}
        self.pads = []
        self.pad  = None

        self.sys_hist = []
        self.sys_bkgs = {}
        self.sys_sigs = {}
        self.error_map= {}
        self.bkg_sum = None

        self.bkg_table = None
        self.sig_table = None

        self.stack    = None
        self.stackeg  = None
        self.leg      = None
        self.legr     = None
        self.texts    = None
        self.ratio    = None
        self.ratioMG  = None        
        self.signif   = None
        self.signifCR = None
        self.err_bands= []
        sum = 0.0

        self.sign.hist.SetLineWidth(2)
        if self.signextra:
            self.signextra.hist.SetLineWidth(2)
            log.info('DrawStack  - integral=%5.2f sample=%s' %(self.signextra.hist.Integral(), 'extrasignal'))
        log.info('DrawStack  - integral=%5.2f sample=%s' %(self.data.hist.Integral(), 'data'))
        log.info('DrawStack  - integral=%5.2f sample=%s' %(self.sign.hist.Integral(), 'signal'))

        for bkg in bkgs:
            self.bkgs[bkg] = self.ReadSample(file, bkg)
            
        for extract_s in extract_sig:
            self.extract_sig[extract_s] = self.ReadSample(file, extract_s)
        sum_err_total = 0.0
        e_double=ROOT.Double(0.0)
        for bkg in bkgs:
            log.info('DrawStack  - integral=%5.2f error=%5.2f mean=%5.2f rms=%5.2f sample=%s' %(self.bkgs[bkg].hist.IntegralAndError(0,10000,e_double), e_double,
                                                                                               self.bkgs[bkg].hist.GetMean(), self.bkgs[bkg].hist.GetRMS(), bkg))
            errdouble = ROOT.Double(0.0)
            sum += self.bkgs[bkg].hist.IntegralAndError(0,10001,errdouble)
            sum_err_total+=errdouble*errdouble
        sum_err_total=math.sqrt(sum_err_total)
        log.info('DrawStack  - integral=%5.2f +/- %5.2f sample=total bkg' %(sum,sum_err_total))

    def GetHistPath(self, sample, syst=None):

        if self.name.count('lim') and options.syst_sel != None:
            histname = '%s_%s_%s' %(sample, self.selkey, options.syst_sel)
        else:
            histname = '/%s/%s_%s/%s' %(self.selkey, self.algkey, sample, self.name)

        if syst != None and options.syst_sel != None:
            histname = histname.replace(options.syst_sel, syst)

        return histname

    def GetNF(self, samples=[], ibin=1):
        madgraph=''
        if options.madgraph:
            madgraph='Mad'
        bkgtotal=0.0
        mc_err=0.0
        signtotal=0.0
        if 'zewk' in samples:
            zcr_bkg_sum = self.GetTotalBkgHist()
            signtotal = self.bkgs['zqcd'+madgraph].hist.GetBinContent(ibin)+self.bkgs['zewk'].hist.GetBinContent(ibin)
            bkgtotal=zcr_bkg_sum.GetBinContent(ibin)-signtotal
            mc_err=zcr_bkg_sum.GetBinError(ibin)
        if 'wewk' in samples:
            wcr_bkg_sum = self.GetTotalBkgHist()            
            signtotal = self.bkgs['wqcd'+madgraph].hist.GetBinContent(ibin)+self.bkgs['wewk'].hist.GetBinContent(ibin)
            bkgtotal=wcr_bkg_sum.GetBinContent(ibin)-signtotal
            mc_err=wcr_bkg_sum.GetBinError(ibin)
            
        datav = self.data.hist.GetBinContent(ibin)
        
        if signtotal>0.0:
            #print 'NF: ',(datav-bkgtotal)/signtotal,' data:',datav,bkgtotal,signtotal
            rel_err = math.sqrt(datav+mc_err**2)/signtotal
            return (datav-bkgtotal)/signtotal,rel_err
        return 1.0,0.0

    def DivideByBinWidth(self,hist):

        if self.name=='jj_mass_variableBin':# or self.name=='jj_mass_variableBinGam':
            for ib in range(2,hist.GetNbinsX()+1):
                wid=hist.GetXaxis().GetBinWidth(ib)
                if (wid<500.0 and wid>100.0) or wid>500.0:
                    expV=hist.GetBinContent(ib)
                    expE=hist.GetBinError(ib)
                    hist.SetBinContent(ib,expV*500.0/wid)
                    hist.SetBinError(ib,expE*500.0/wid)
    
    def ReadSample(self, file, sample, syst=None, DO_SYMM=False):

        path = self.GetHistPath(sample, syst)
        #print path
        hist = file.Get(path)
        #hist
        #if var=="jj_mass":
        
        if not hist:
            file.ls()
            raise KeyError('DrawStack - missing histogram: file=%s hist=%s' %(file.GetPath(), path))

        log.debug('ReadSample - integral=%5.1f sample=%s, syst=%s' %(hist.Integral(), sample, syst))
        hist=hist.Clone()
        # adding post fit electron fakes
        if options.add_fakeE and (sample=='tth' or sample=='vbfg'):
            #antiELowMET, scale 7.1
            if 'jj_mass_variableBin' in self.name:
                hist.SetBinContent(4,44.4+38.4+28.); hist.SetBinError(4,25.0)
                hist.SetBinContent(5,32.2+34.4+12.); hist.SetBinError(5,22.0)
                hist.SetBinContent(6,7.4+8.5); hist.SetBinError(4,6.0)
                hist.SetBinContent(7,9.2+19.5); hist.SetBinError(4,15.0)
                hist.SetBinContent(8,2.8+0.6); hist.SetBinError(4,2.0)
                
            if 'jj_mass_variableBinGam' in self.name:
                #hist.SetBinContent(2,1.9);  hist.SetBinError(2,0.5)
                hist.SetBinContent(2,0.5);  hist.SetBinError(2,0.5)                
                hist.SetBinContent(3,0.2);  hist.SetBinError(3,0.25)
                hist.SetBinContent(4,0.15); hist.SetBinError(4,0.15)
                hist.SetBinContent(5,0.1);  hist.SetBinError(5,0.07)
                hist.SetBinContent(6,0.05); hist.SetBinError(6,0.03)
                # adds the fake met bkg also
                hist.SetBinContent(4,0.45); hist.SetBinError(4,0.15)
                hist.SetBinContent(5,0.4);  hist.SetBinError(5,0.07)
                hist.SetBinContent(6,0.05); hist.SetBinError(6,0.03)                
                #hist.Scale(45.0/7.1)
                #hist.Scale(90.0/7.1)
                hist.Scale(350.0/7.1)
                #hist.Scale(25.0/7.1)                
            if 'jj_dphi' in self.name:
                for  ij in range(1,11):
                    hist.SetBinContent(ij,23.0/2.0); hist.SetBinError(ij,4.0)
                    hist.SetBinContent(ij+10,24.9/2.0); hist.SetBinError(ij+10,4.0)
                if options.ph_ana:
                    for  ij in range(1,15):
                        hist.SetBinContent(ij,5.0/2.0); hist.SetBinError(ij,1.0)
                        hist.SetBinContent(ij+10,3/2.0); hist.SetBinError(ij+10,4.0)                    
            if 'met_tst_nolep_et' in self.name:
                for  ij in range(21,26):
                    hist.SetBinContent(ij,100.0/5.0); hist.SetBinError(ij,20.0/5.0)
                    hist.SetBinContent(ij+5,60.0/5.0); hist.SetBinError(ij+4,20.0/5.0)
                    hist.SetBinContent(ij+10,45.0/5.0); hist.SetBinError(ij+10,10.0/5.0)
                    hist.SetBinContent(ij+15,20/5.0); hist.SetBinError(ij+15,8.0/5.0)
                    hist.SetBinContent(ij+20,13/5.0); hist.SetBinError(ij+20,5.0/5.0)
                    hist.SetBinContent(ij+25,1/5.0); hist.SetBinError(ij+25,0.5/5.0)
                
        self.DivideByBinWidth(hist)
        if DO_SYMM and not ( options.add_fakeE and (sample=='tth' or sample=='vbfg')):
            nom_path = self.GetHistPath(sample, 'Nominal')            
            #print 'COMPUTING systematic',nom_path
            hist_central_value = self.file_pointer.Get(nom_path)
            hist_central_value=hist_central_value.Clone()
            self.DivideByBinWidth(hist_central_value)
            self.Symmeterize(hist_central_value, hist)

        return HistEntry(hist, sample, self.name, self.nf_map, self.zcr_stack, self.wcr_stack)

    #------------------------
    def Symmeterize(self, hnom, hvar):
        #
        # Symmeterize(nominal_histogram, variation_histogram)
        #    This function symmeterizes the systematics for the track met
        #       using the lognormal variation: Nominal/Up_variation
        #    The variations for var/nom<0.5 are treated special so that very
        #       large variations do not occur because of low MC stats.
        for i in range(0,hnom.GetNbinsX()+1):
            diff_up = 1.0
            if hnom.GetBinContent(i)>0.0 and hvar.GetBinContent(i)>0.0:
                diff_up = hvar.GetBinContent(i)/hnom.GetBinContent(i)
                if diff_up<0.5:
                    diff_up=0.5
            hvar.SetBinContent(i, (1.0/diff_up)*hnom.GetBinContent(i)) # this is:  nominal * (nominal / up_variation)

    #-------------------------
    def ReadSystFiles(self, sfiles):

        for syst, sfile in sfiles.iteritems():
            print 'SYST:',syst
            # check if we need to symmeterize
            DO_SYMM=False
            syst_key = copy.deepcopy(syst)
            if syst in symm_list:
                DO_SYMM=True
                print 'Symmeterize: ',syst
                #print 'DOWN Map:',mysystOneSided.getsystematicsOneSidedMap()
                if syst in mysystOneSided.getsystematicsOneSidedMap():
                    #print 'In map: ',syst
                    syst_key = mysystOneSided.getsystematicsOneSidedMap()[syst]

            bkg_ent = None

            for bkg in self.bkgs:
                bhist = self.ReadSample(sfile, bkg, syst_key, DO_SYMM=DO_SYMM)
                #if options.syst_type=='MJsyst' and bkg in ['zqcd','zewk','wqcd','z']
                if bkg_ent == None:
                    bkg_ent = bhist
                else:
                    bkg_ent.hist.Add(bhist.hist)
            if bkg_ent == None:
                log.warning('ReadSysts - missing background syst histograms: %s' %syst)
                sys.exit(1)

            bkg_ent.sample = 'bkgs'
            self.sys_bkgs[syst] = bkg_ent
            print syst,'integral: ',bkg_ent.hist.Integral()
            self.sys_sigs[syst] = self.ReadSample(sfile, self.sign.sample, syst_key, DO_SYMM=DO_SYMM)

    #-------------------------
    def GetTotalBkgHist(self):

        bhist = None

        for bkg, ent in self.bkgs.iteritems():
            if bhist == None:
                bhist = ent.hist.Clone()
                bhist.SetDirectory(0)
            else:
                #print bkg,ent.hist.Integral()
                bhist.Add(ent.hist)

        return bhist

    #--------------------------
    def PrintBkgSystYields(self):

        sum_nom = 0.0
        sum_sys = []

        for bkg, ent in self.bkgs.iteritems():
            sum_nom += ent.hist.Integral()

        for sys, ent in self.sys_bkgs.iteritems():
            sum_sys += [(sys, ent.hist.Integral(), sum_nom)]

        log.info('PrintBkgSystYields - sum_nom=%3.1f' %(sum_nom))

        for value in sorted(sum_sys, key=getSystSumSortKey):
            log.info('                     sum_sys=%3.1f %s' %(value[1], value[0]))

        h = ROOT.TH1D('bkg_syst', 'bkg_syst', len(sum_sys), 0.0, len(sum_sys))
        h.SetDirectory(0)

        if sum_nom > 0.0:
            sum_sys = sorted(sum_sys, key = lambda val: val[0])

            for i in range(0, len(sum_sys)):
                sum = sum_sys[i]
                h.SetBinContent(i+1, sum[1]/sum_nom)
                h.GetXaxis().SetBinLabel(i+1, sum[0])
        return h

    #----------------------
    def PrintSigSystYields(self):

        sum_nom = self.sign.hist.Integral()
        sum_sys = []

        for sys, ent in self.sys_sigs.iteritems():
            sum_sys += [(sys, ent.hist.Integral(), sum_nom)]

        log.info('PrintSigSystYields - sum_nom=%3.1f' %(sum_nom))

        for value in sorted(sum_sys, key=getSystSumSortKey):
            log.info('                     sum_sys=%3.1f %s' %(value[1], value[0]))

        h = ROOT.TH1D('sig_syst', 'sig_syst', len(sum_sys), 0.0, len(sum_sys))
        h.SetDirectory(0)

        if sum_nom > 0.0:
            sum_sys = sorted(sum_sys, key = lambda val: val[0])

            for i in range(0, len(sum_sys)):
                sum = sum_sys[i]
                h.SetBinContent(i+1, sum[1]/sum_nom)
                syst_name_map=syst_names()
                my_name=sum[0]
                if sum[0] in syst_name_map:
                    my_name=syst_name_map[sum[0]]
                h.GetXaxis().SetBinLabel(i+1, my_name)

        return h

    #------------------------
    def GetBkgSystBinError(self, ibin):

        cbin = 0.0
        cval = 0.0
        cerr = 0.0

        for bkg, ent in self.bkgs.iteritems():
            if ibin >= 0 and ibin <= ent.hist.GetNbinsX()+1:
                cval += ent.hist.GetBinContent(ibin)
                cbin  = ent.hist.GetBinCenter (ibin)

        for sys, ent in self.sys_bkgs.iteritems():
            if ibin >= 0 and ibin <= ent.hist.GetNbinsX()+1:
                sval = ent.hist.GetBinContent(ibin)
                cerr += (cval-sval)*(cval-sval)

                ratio = 0.0
                if cval > 0.0:
                    ratio = sval/cval

                log.debug('GetBkgSystBinError - bin=%3d center=%6.1f val=%3.2f: sval=%3.2f ratio=%1.2f syst=%s' %(ibin, cbin, cval, sval, ratio, sys))

        return (cval, math.sqrt(cerr))

    #------------------------
    def PlotSystSig(self, syst, can):
        if syst not in self.sys_sigs:
            return None

        log.info('PlotSystSig - %s: %s' %(self.name, syst))

        sys = self.sys_sigs[syst].hist.Clone()
        sig = self.sign.hist.Clone()

        sig.SetLineWidth(2)
        sys.SetLineWidth(2)

        sig.SetLineColor(1)
        sys.SetLineColor(2)

        hpars = getHistPars(self.name)
        sys.GetXaxis().SetTitle(hpars['xtitle'])
        sys.GetXaxis().CenterTitle()

        sig_sum = sig.Integral()
        sys_sum = sys.Integral()

        log.info('   draw ratio')
        sys.Divide(sig)

        if math.fabs(sys.GetMinimum()-1.0) < 0.05 and math.fabs(sys.GetMaximum()-1.0) < 0.05:
            sys.GetYaxis().SetRangeUser(0.94, 1.06)
        elif math.fabs(sys.GetMinimum()-1.0) < 0.15 and math.fabs(sys.GetMaximum()-1.0) < 0.15:
            sys.GetYaxis().SetRangeUser(0.80, 1.20)            
        elif math.fabs(sys.GetMinimum()-1.0) < 0.7 and math.fabs(sys.GetMaximum()-1.0) < 0.7:
            sys.GetYaxis().SetRangeUser(0.20, 1.80)
        else:
            sys.GetYaxis().SetRangeUser(0.0, 3.0)
        sys.GetYaxis().SetRangeUser(0.7, 1.3)

        sys.GetYaxis().SetTitle('Nominal/%s' %syst)
        sys.GetYaxis().CenterTitle()
        if options.draw_norm: sys.DrawNormalized('HIST')
        else: sys.Draw('HIST')

        t = '#splitline{Nominal: %.3f}{%s: %.3f}' %(sig_sum, syst, sys_sum)
        l = ROOT.TLatex(0.5, 0.85, t)
        l.SetNDC()
        l.SetTextFont(42)
        l.SetTextSize(0.04)
        l.SetTextAlign(11)
        l.SetTextColor(ROOT.kBlack)
        l.Draw()

        p = getSelKeyLabel(options.selkey) + ' (signal)'
        if p != None:
            c = ROOT.TLatex(0.2, 0.96, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)

        updateCanvas(can, name='%s_%s_%s_sig' %(getSelKeyPath(), self.name, syst, self.data, self.bkg_sum))

    #----------------------
    def PlotSystBkg(self, syst, can):
        if syst not in self.sys_bkgs:
            return None

        log.info('PlotSystBkg - %s: %s' %(self.name, syst))

        sys = self.sys_bkgs[syst].hist.Clone()
        bkg = self.GetTotalBkgHist()

        bkg.SetLineWidth(2)
        sys.SetLineWidth(2)

        bkg.SetLineColor(1)
        sys.SetLineColor(4)

        bkg.SetFillColor(0)
        bkg.SetFillStyle(0)

        sys.SetFillColor(0)
        sys.SetFillStyle(0)

        hpars = getHistPars(self.name)
        sys.GetXaxis().SetTitle(hpars['xtitle'])
        sys.GetXaxis().CenterTitle()

        bkg_sum = bkg.Integral()
        sys_sum = sys.Integral()

        sys.Divide(bkg)
        log.info('   draw bkg ratio: min/max = %.2f/%.2f' %(sys.GetMinimum(), sys.GetMaximum()))

        if math.fabs(sys.GetMinimum()-1.0) < 0.05 and math.fabs(sys.GetMaximum()-1.0) < 0.05:
            sys.GetYaxis().SetRangeUser(0.94, 1.06)
        elif math.fabs(sys.GetMinimum()-1.0) < 0.15 and math.fabs(sys.GetMaximum()-1.0) < 0.15:
            sys.GetYaxis().SetRangeUser(0.80, 1.20)
        elif math.fabs(sys.GetMinimum()-1.0) < 0.7 and math.fabs(sys.GetMaximum()-1.0) < 0.7:
            sys.GetYaxis().SetRangeUser(0.0, 1.80)
        else:
            sys.GetYaxis().SetRangeUser(0.0, 3.0)
        #sys.GetYaxis().SetRangeUser(0.7, 1.3)

        sys.GetYaxis().SetTitle('%s/Nominal' %syst)
        sys.GetYaxis().CenterTitle()

        if options.draw_norm: sys.DrawNormalized('HIST')
        else:  sys.Draw('HIST')

        t = '#splitline{Nominal: %.2f}{%s: %.2f}' %(bkg_sum, syst, sys_sum)
        l = ROOT.TLatex(0.5, 0.85, t)
        l.SetNDC()
        l.SetTextFont(42)
        l.SetTextSize(0.04)
        l.SetTextAlign(11)
        l.SetTextColor(ROOT.kBlack)
        l.Draw()

        p = getSelKeyLabel(options.selkey) + ' (sum of backgrounds)'
        if p != None:
            c = ROOT.TLatex(0.2, 0.96, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)

        updateCanvas(can, name='%s_%s_%s_bkg' %(getSelKeyPath(), self.name, syst, self.data, self.bkg_sum))

    #-------------------
    def PlotManySyst(self, systs, can, isSignal=False, fillData=False, groupStart=-1, groupEnd=-1):
        #if syst not in self.sys_bkgs:
        #    return None
        if len(self.pads)>1:
            self.pads[0].Clear()
            self.pads[1].Clear()
            self.pads[0].cd()
            self.pads[0].SetBottomMargin(0.15);
        sys=[]
        ratio_sys = []
        iSys=0
        for s in systs:
            if groupStart>0 and iSys<groupStart:
                iSys+=1
                continue
            if isSignal:
                sys       += [self.sys_sigs[s].hist.Clone()]
                ratio_sys += [self.sys_sigs[s].hist.Clone()]
            else:
                sys       += [self.sys_bkgs[s].hist.Clone()]
                ratio_sys += [self.sys_bkgs[s].hist.Clone()]
            iSys+=1
            if groupEnd>0 and iSys>groupEnd:
                break;
        mydata=None
        if fillData:
            mydata = self.data.hist.Clone()
            mydata.SetLineWidth(2)
            mydata.SetLineColor(1)
            mydata.SetFillColor(0)
            mydata.SetFillStyle(0)

        bkg = self.GetTotalBkgHist()
        if isSignal:
            bkg = self.sign.hist.Clone()
            bkg.SetDirectory(0)
        bkg.SetLineWidth(2)
        bkg.SetLineColor(2)
        bkg.SetFillColor(0)
        bkg.SetFillStyle(0)

        hpars = getHistPars(self.name)

        bkg.GetXaxis().SetTitle(hpars['xtitle'])
        bkg.GetYaxis().SetTitle(hpars['ytitle'])
        max_bin = bkg.GetMaximum()
        # Set the systematics plots
        tmp_color=3
        i=0
        for s in sys:
            if not s:
                print  'not a valid hist: ',s
                continue
            log.info('PlotManySyst - %s: %s Mean: %0.2f RMS: %0.2f' %(self.name, systs[i], s.GetMean(), s.GetRMS()))
            s.SetLineColor(getColor(tmp_color))
            s.SetMarkerColor(getColor(tmp_color))
            s.SetLineWidth(2)
            s.SetFillColor(0)
            s.SetFillStyle(0)
            tmp_color+=1
            i+=1
            if max_bin<s.GetMaximum():
                max_bin = s.GetMaximum()

        bkg.GetYaxis().SetRangeUser(0.0, 0.35*max_bin)
        self.UpdateHist(bkg, ignore_max=False)
        bkg.Draw('HIST E0')
        bkg.SetMarkerSize(0)
        if fillData:
            mydata.SetMarkerSize(0)
            mydata.Draw('SAME')
        for s in sys:
            s.SetMarkerSize(0)
            s.Draw('HIST SAME')

        p = getSelKeyLabel(options.selkey) + ' (sum of backgrounds)'
        if isSignal:
            p = getSelKeyLabel(options.selkey) + ' (sum of signal)'
        if p != None:
            c = ROOT.TLatex(0.2, 0.96, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)
            c.Draw()
        self.texts = getATLASLabels(can, 0.2, 0.86, selkey=self.selkey)
        for text in self.texts:
            text.Draw()

        self.leg = ROOT.TLegend(0.58, 0.55, 0.93, 0.89)
        self.leg.SetBorderSize(0)
        self.leg.SetFillStyle (0)
        #if var=="jj_mass":
        self.leg.SetTextFont(42);
        self.leg.SetTextSize(0.04);
        if fillData:
            self.leg.AddEntry(mydata, 'Data')
        self.leg.AddEntry(bkg,    'Nominal')
        i=0
        j=0
        while i<len(systs):
            if groupStart>0 and i<groupStart:
                i+=1
                continue

            self.leg.AddEntry(sys[j],systs[i])
            i+=1
            j+=1
            if groupEnd>0 and i>groupEnd:
                break
        self.leg.Draw()

        # Draw the ratios
        if len(self.pads)>1:
            self.pads[1].cd()

            # Set the ratio histograms
            tmp_color=3
            bkg_ratio=bkg.Clone()
            if fillData:
                bkg_ratio.Divide(mydata)
            for s in ratio_sys:

                # Divide
                if fillData:
                    s.Divide(mydata)
                else:
                    s.Divide(bkg)

                # SetRange
                if math.fabs(s.GetMinimum()-1.0) < 0.025 and math.fabs(s.GetMaximum()-1.0) < 0.025:
                    s.GetYaxis().SetRangeUser(0.975, 1.025)
                elif math.fabs(s.GetMinimum()-1.0) < 0.05 and math.fabs(s.GetMaximum()-1.0) < 0.05:
                    s.GetYaxis().SetRangeUser(0.95, 1.05)
                elif math.fabs(s.GetMinimum()-1.0) < 0.15 and math.fabs(s.GetMaximum()-1.0) < 0.15:
                    s.GetYaxis().SetRangeUser(0.80, 1.20)
                elif math.fabs(s.GetMinimum()-1.0) < 0.5 and math.fabs(s.GetMaximum()-1.0) < 0.5:
                    s.GetYaxis().SetRangeUser(0.501, 1.499)
                elif math.fabs(s.GetMinimum()-1.0) < 1.0 and math.fabs(s.GetMaximum()-1.0) < 1.0:
                    s.GetYaxis().SetRangeUser(0.0, 2.00)
                else:
                    s.GetYaxis().SetRangeUser(0.0, 3.0)

                # Style
                s.SetLineColor(getColor(tmp_color))
                s.SetMarkerColor(getColor(tmp_color))
                s.SetLineWidth(2)
                s.SetFillColor(0)
                s.SetFillStyle(0)
                if fillData:
                    s.GetYaxis().SetTitle('%s / Data' %'Syst')
                    if tmp_color==3:
                        self.UpdateHist(bkg_ratio)
                        bkg_ratio.GetYaxis().SetTitle('%s / Data' %'Syst')
                        bkg_ratio.GetYaxis().SetRangeUser(0.80, 1.20)
                        bkg_ratio.Draw('HIST')
                else:
                    s.GetYaxis().SetTitle('%s / Nominal' %'Syst')
                s.GetYaxis().CenterTitle()
                tmp_color+=1

                if tmp_color==4 and not fillData:
                    self.UpdateHist(s,ignore_max=True)
                    s.GetYaxis().SetRangeUser(0.95, 1.05)
                    s.Draw('HIST')
                else:
                    s.Draw('HIST SAME')

        if isSignal:
            updateCanvas(can, name='%s_%s_%s%s_sig' %(getSelKeyPath(), self.name, 'systall',groupStart))
        else:
            updateCanvas(can, name='%s_%s_%s%s_bkg' %(getSelKeyPath(), self.name, 'systall',groupStart))

    #------------------------------
    def PlotSystTables(self, can):

        self.bkg_table = self.PrintBkgSystYields()
        self.sig_table = self.PrintSigSystYields()

        if self.bkg_table == None or self.sig_table == None:
            return

        #
        # Draw background
        #
        self.bkg_table.SetFillStyle(2001)
        self.bkg_table.SetFillColor(4)

        self.bkg_table.SetStats(False)
        self.bkg_table.GetYaxis().SetRangeUser(0.82, 1.18)

        self.bkg_table.GetYaxis().SetTitle('Systematics/Nominal')
        self.bkg_table.GetYaxis().CenterTitle()
        self.bkg_table.GetYaxis().SetTitleOffset(1.0)
        self.bkg_table.GetYaxis().SetTitleSize(0.05)
        self.bkg_table.GetYaxis().SetLabelSize(0.05)
        self.bkg_table.GetXaxis().SetLabelSize(0.05)

        if options.draw_norm: self.bkg_table.DrawNormalized('HBAR')
        else: self.bkg_table.Draw('HBAR')

        p = getSelKeyLabel(options.selkey)
        if p != None:
            p +=  ' (backgrounds)'
            c = ROOT.TLatex(0.30, 0.95, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)

        updateCanvas(can, name='%s_%s_bkg_table' %(getSelKeyPath(), self.name))

        #
        # Draw signal
        #
        self.sig_table.SetFillStyle(2001)
        self.sig_table.SetFillColor(2)

        self.sig_table.SetStats(False)
        #self.sig_table.GetYaxis().SetRangeUser(0.82, 1.18)
        self.sig_table.GetYaxis().SetRangeUser(0.95, 1.05)

        self.sig_table.GetYaxis().SetTitle('Systematics/Nominal')
        self.sig_table.GetYaxis().CenterTitle()
        self.sig_table.GetYaxis().SetTitleOffset(1.0)
        self.sig_table.GetYaxis().SetTitleSize(0.05)
        self.sig_table.GetYaxis().SetLabelSize(0.05)
        self.sig_table.GetXaxis().SetLabelSize(0.05)

        my_line = ROOT.TLine(1.0,0,1.0,len(self.sys_sigs))
        my_line.SetLineColor(1)
        my_line.SetLineWidth(3)
        my_line.SetLineStyle(2)
        my_line.Draw('same')
        p = getSelKeyLabel(options.selkey)
        if p != None:
            p += ' (signal)'
            c = ROOT.TLatex(0.30, 0.95, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)

        updateCanvas(can, name='%s_%s_sig_table' %(getSelKeyPath(), self.name))
    #-------------------------------------
    def IsLogy(self):
        if options.do_logy: return True
        if options.no_logy: return False

        if self.sign != None and self.sign.logy:
            return True
        if self.signextra != None and self.signextra.logy:
            return True
        if self.data != None and self.data.logy:
            return True

        return False

    #-------------------------------------
    def GetErrorHists(self):
        bkg_herr = self.stack.GetHistogram().Clone()
        norm_hists_bkg=[]
        for hk,hg in self.bkgs.iteritems():
            norm_hists_bkg+=[hg.hist.Clone()]
            bkg_herr.Add(hg.hist)
        return norm_hists_bkg,bkg_herr

    #-------------------------------------
    def Draw(self, can):
        log.info('DrawStack - draw: %s' %self.name)

        # Allow legend location to be overriden on the command line.
        # To change defaults; edit option parser arguments above.
        self.leg = ROOT.TLegend(*options.legend_coords)
        if False:
            #self.leg = ROOT.TLegend(0.51, 0.60, 0.915, 0.855)
            self.leg = ROOT.TLegend(0.55, 0.60, 0.94, 0.9)
            #self.leg = ROOT.TLegend(0.50, 0.60, 0.92, 0.84)
            self.leg.SetNColumns  (2)           
        # Also allow the user to switch back to one column for some plots.
        self.leg.SetNColumns(options.legend_cols)
        self.leg.SetBorderSize(0)
        self.leg.SetFillStyle (0)
        self.leg.SetTextFont(42);
        self.leg.SetTextSize(0.04);
        self.leg1= ROOT.TLegend(0.59, 0.52, 0.85, 0.67)
        self.leg1.SetBorderSize(0)
        self.leg1.SetFillStyle (0)
        self.leg1.SetTextFont(42);
        self.leg1.SetTextSize(0.04);
        self.pads=[]
        can.cd()
        if options.do_ratio or options.force_ratio:
            # CAF setup
            ratioPadRatio  = 0.3;
            markerSize = 1;
            lineWidth = 2;
            markerStyle = 20;
            padScaling      = 0.75 / (1. - ratioPadRatio) ;
            ratioPadScaling = 0.75*(1. / ratioPadRatio) ;
            ROOT.gStyle.SetPadTopMargin(0.065);
            ROOT.gStyle.SetPadRightMargin(0.05);
            ROOT.gStyle.SetPadBottomMargin(0.16);
            ROOT.gStyle.SetPadLeftMargin(0.16);
            ROOT.gStyle.SetTitleXOffset(1.0);
            ROOT.gStyle.SetTitleYOffset(1.28);
            self.pads.append( ROOT.TPad('pad0','pad0', 0.0, ratioPadRatio, 1.0, 1.0) )
            self.pads.append( ROOT.TPad('pad1','pad1', 0.0, 0.0, 1.0, ratioPadRatio) )

            self.pads[0].SetTopMargin(padScaling * self.pads[0].GetTopMargin());
            self.pads[0].SetBottomMargin(.015);
            self.pads[0].SetTickx(True);
            self.pads[0].SetTicky(True);
            #self.pads[1].SetTopMargin(.01);
            self.pads[1].SetBottomMargin(.4);
            #self.pads[1].SetBottomMargin(ratioPadScaling * self.pads[1].GetBottomMargin());
            self.pads[1].SetGridy(True);
            self.pads[1].SetTickx(True);
            self.pads[1].SetTicky(True);

            self.legr= ROOT.TLegend(0.07, 0.01, 0.35, 0.28)
            self.legr.SetBorderSize(0)
            self.legr.SetFillStyle (0)
            self.legr.SetTextFont(42);
            self.legr.SetTextSize(0.09);
            if False:
                self.pads[0].SetTicky(0)
                # Margins
                tmargin = 0.05
                lmargin = 0.15
                rmargin = 0.28
                bmargin = 0.18

                for pad in self.pads:
                    pad.SetFrameLineColor(0)
                    pad.SetLeftMargin(lmargin)
                    pad.SetRightMargin(rmargin)
                    pad.SetTopMargin(tmargin+bmargin)
                    pad.SetBottomMargin(bmargin-0.03)
                    pad.SetFillColor(0)
                    pad.SetFillStyle(0)
                    pad.Draw()
                if len(self.pads)>1:
                    rmargin_ = 0.2
                    self.pads[0].SetTopMargin(tmargin+bmargin)
                    self.pads[0].SetRightMargin(rmargin_)
                    self.pads[0].SetBottomMargin(0.0)
                    self.pads[1].SetTopMargin(0.0)
                    self.pads[1].SetBottomMargin(tmargin+bmargin)
                    self.pads[1].SetFrameLineColor(1)
                    self.pads[1].SetRightMargin(rmargin_)
                    self.pads[1].SetTicky(1) # RHS ticks
            else:
                if len(self.pads)>1:
                    self.pads[0].SetBottomMargin(0.0)
                    self.pads[1].SetTopMargin(0.0)
                self.pads[0].Draw()
                self.pads[1].Draw()

            ipad = 0
            self.pad = self.pads[ipad]
            self.pad.cd()

        if self.IsLogy():
            can.SetLogy(1)
            if options.do_ratio:
                self.pads[0].SetLogy(1)
        else:
            can.SetLogy(0)

        self.CreateStack()

        if options.draw_norm: self.bkg_sum.DrawNormalized('HIST')
        else:                 self.stack.Draw('HIST')

        if not options.stack_signal and not options.no_signal:
            self.UpdateHist(self.sign.hist,self.sign.sample)
            self.sign.DrawHist('SAME HIST', self.leg, True)
        if self.signextra:
            self.UpdateHist(self.signextra.hist,self.signextra.sample)
            self.signextra.DrawHist('SAME HIST', self.leg, True)
        self.UpdateStack()
        if options.do_ratio or options.force_ratio:
            #self.UpdateStack()
            bx = self.stack.GetXaxis();
            by = self.stack.GetYaxis();
            #if not options.draw_norm:
            #    bx = self.bkg_sum.GetXaxis();
            #    by = self.bkg_sum.GetYaxis();
            bx.SetTitleSize(ROOT.gStyle.GetTitleSize("x") * padScaling);
            bx.SetLabelSize(ROOT.gStyle.GetLabelSize("x") * padScaling);
            by.SetTitleSize(ROOT.gStyle.GetTitleSize("y") * padScaling);
            by.SetTitleOffset(ROOT.gStyle.GetTitleOffset("y") / padScaling  );
            by.SetLabelSize(ROOT.gStyle.GetLabelSize("y") * padScaling);
            bx.SetLabelColor(0);
            bx.SetTickLength(bx.GetTickLength() * padScaling);
            #print 'OFFSET'
            bx.SetLabelOffset(1.2);
            bx.SetLabelSize(0.03);
            bx.SetTitle("")
            #bx.SetTitle("")
            by.SetRangeUser(0,80);
            by.SetTitleSize(0.055);
            by.SetTitleOffset(1.28);
            by.SetLabelSize(0.05);
            by.SetLabelOffset(0.01);


        # Add Data
        if self.data != None and not options.blind:
            #self.data.hist.GetXaxis().SetLabelColor(0)
            self.data.hist.GetXaxis().SetTitle("")
            self.data.DrawHist('SAME', None)

        if True:
            self.bkg_sum.SetLineColor(ROOT.kRed)
            self.bkg_sum.SetLineWidth(0)
            self.bkg_sum.SetFillColor(0)
            self.bkg_sum.GetXaxis().SetLabelColor(0)
            if options.draw_norm: self.bkg_sum.DrawNormalized('HIST SAME')
            else: self.bkg_sum.Draw('HIST SAME')
            self.bkg_sum_alt=self.bkg_sum.Clone()
            self.bkg_sum_alt.SetLineColor(ROOT.kRed)
            self.bkg_sum_alt.SetMarkerColor(ROOT.kRed)
            self.bkg_sum_alt.SetMarkerSize(0)
            self.bkg_sum_alt.SetFillColor(1)
            self.bkg_sum_alt.SetFillStyle(3345) #3004
            
        self.leg.Draw()
        self.leg1.Draw()

        self.texts = getATLASLabels(can, 0.19, 0.83+0.02, selkey=self.selkey)
        for text in self.texts:
            text.Draw()

        if self.data.text1st != None:
            log.info('Draw 1st bin text...')
            self.data.text1st.Draw()

        #
        # Draw systematics error band around total background stack
        #    - this isn't used. It is commented out. it assumes a systemtic uncertainty
        if options.draw_syst:
            bkg_herr = self.stack.GetHistogram().Clone()
            bkg_herr.GetXaxis().SetLabelColor(0)
            bkg_herr.GetXaxis().SetTitle("")
            for ibin in range(1, bkg_herr.GetNbinsX()+1):
                val, err = self.GetBkgSystBinError(ibin)
                bkg_herr.SetBinContent(ibin, val)
                bkg_herr.SetBinError  (ibin, err)

            self.stackeg = ROOT.TGraphAsymmErrors(bkg_herr)

            #self.stackeg.SetFillStyle(3005)
            self.stackeg.SetFillStyle(3345) # 3004
            self.stackeg.SetFillColor(1)
            self.stackeg.GetXaxis().SetLabelColor(0)
            #self.stackeg.Draw('2')
        #
        # Draw chi2 for stack and data
        #
        if options.do_ks and not options.blind:
            chi2 = self.data.hist.Chi2Test      (self.bkg_sum, 'UW CHI2')
            kval = self.data.hist.KolmogorovTest(self.bkg_sum, '')

            log.info('Draw - %s: chi2 = %.2f' %(self.name, chi2))
            log.info('Draw - %s: KS   = %.2f' %(self.name, kval))

            self.ks_text = ROOT.TLatex(0.3, 0.95, 'KS: %.2f' %kval)
            self.ks_text.SetNDC()
            self.ks_text.SetTextSize(0.055)
            self.ks_text.SetTextAlign(11)
            self.ks_text.SetTextColor(ROOT.kBlack)
            self.ks_text.Draw()
            
        # Plot - calculating the systematic error bands
        norm_hists_bkg=[]
        for hk,hg in self.bkgs.iteritems(): norm_hists_bkg+=[hg.hist.Clone()]
        syst_hist_bkg=ROOT.TGraphAsymmErrors(self.bkg_sum); self.err_bands+=[syst_hist_bkg]
        syst_ratio=syst_hist_bkg.Clone(); self.err_bands+=[syst_ratio]
        syst_jes_ratio = self.SystBand(norm_hists_bkg, syst=syst_hist_bkg, syst_ratio=syst_ratio, linestyle=0, tot_bkg=self.bkg_sum, other_syst=None) #other_syst=self.stackeg

        # Setting the draw options
        syst_hist_bkg.SetFillStyle(3345) #3004
        syst_hist_bkg.SetFillColor(12)
        syst_hist_bkg.SetMarkerColor(1)
        syst_hist_bkg.SetLineColor(1)
        syst_hist_bkg.GetXaxis().SetLabelColor(0)
        self.error_map['bkg']=syst_hist_bkg.Clone()
        self.error_map['bkg'].GetXaxis().SetLabelColor(0)
        self.error_map['bkg'].SetFillStyle(3345) #3004
        self.error_map['bkg'].SetFillColor(ROOT.kBlack)
        self.error_map['bkg'].SetMarkerColor(1)
        self.error_map['bkg'].SetMarkerSize(0)
        self.error_map['bkg'].SetLineColor(1)
        if options.draw_norm: pass #self.error_map['bkg'].DrawNormalized('SAMEE2')
        else: self.error_map['bkg'].Draw('SAMEE2')

        # Draw Arrow
        if self.name in ['mjj','ptll_over_met','ptj0_over_met']:
            cut = 1.9
            if self.name=='mjj':
                cut=350.0
            if self.name=='ptll_over_met':
                cut=0.4
            if self.name=='ptj0_over_met':
                cut=1.9
            self.arrow = ROOT.TArrow( cut, 0.2, cut, 0.0, 0.04, '|>' )
            self.arrow.SetFillStyle( 1001 )
            self.arrow.SetLineColor( ROOT.kRed )
            self.arrow.SetFillColor( ROOT.kRed )
            self.arrow.Draw()
            self.my_line2 = ROOT.TLine(cut,0.0,cut,0.3*self.stack.GetMaximum())
            if options.do_logy:
                self.my_line2 = ROOT.TLine(cut,0.0,cut,0.06*self.stack.GetMaximum())
            self.my_line2.SetLineColor(ROOT.kRed)
            self.my_line2.SetLineWidth(2)
            self.my_line2.SetLineStyle(1)
            self.my_line2.Draw('same')

        if options.do_ratio or options.force_ratio:
            # Ratio
            ipad = 1
            #self.pad = self.pads[ipad]
            #self.pad.cd()
            self.pads[ipad].cd()
            if options.blind:
                self.ratio=self.sign.hist.Clone()
                self.ratioMG=self.sign.hist.Clone()                
                self.signif=self.sign.hist.Clone()
                self.signifCR=self.sign.hist.Clone()
                self.signif.SetMinimum(0.0)
                self.signif.SetMaximum(2.0)
            else:
                self.ratio=self.data.hist.Clone()
                self.ratioMG=self.data.hist.Clone()
            self.UpdateHist(self.ratio)
            self.UpdateHist(self.ratioMG)
            self.ratio.SetMinimum(0.25)
            self.ratio.SetMaximum(1.75)

            if options.do_nf!=None:
                samples = options.do_nf.split(',')
                if options.blind:
                    self.ratio=self.sign.hist.Clone()
                    self.ratioMG=self.sign.hist.Clone()
                    self.signif=self.sign.hist.Clone()
                    self.signifCR=self.sign.hist.Clone()
                else:
                    self.ratio=self.data.hist.Clone()
                den=None
                tot_bkg=0.0; tot_data=0.0;
                tot_data=self.ratio.Integral(4,101)

                for bkg, ent in self.bkgs.iteritems():
                    if bkg in samples:
                        if den==None:
                            den=ent.hist.Clone()
                        else:
                            den.Add(ent.hist)
                    else:
                        self.ratio.Add(ent.hist, -1.0)
                        self.ratioMG.Add(ent.hist, -1.0)
                        tot_bkg+=ent.hist.Integral(4,101)

                # set MC error to zero.
                den_tmp=den.Clone() # removing the mc stat uncertainty from the ratio...
                if options.show_mc_stat_err:
                    for i in range(0,den_tmp.GetNbinsX()):
                        den_tmp.SetBinError(i,0.0)
                self.ratio.Divide(den_tmp)
                for i in range(0,self.ratio.GetNbinsX()+1):
                    if i<6:
                        print self.ratio.GetXaxis().GetBinLowEdge(i),' mean: ',self.ratio.GetBinContent(i),' +/- ',self.ratio.GetBinError(i)

            else:
                # set MC error to zero.
                den_tmp=self.bkg_sum.Clone() # removing the mc stat uncertainty from the ratio...
                if options.show_mc_stat_err:
                    for i in range(0,den_tmp.GetNbinsX()):
                        den_tmp.SetBinError(i,0.0)
                self.ratio.Divide(den_tmp)

                # add MG mjj...do for Wg strong and Zg strong
                if options.mg_ratio:
                    mg_den_tmp = den_tmp.Clone()
                    for bkg, ent in self.bkgs.iteritems():
                        if bkg in ["zgam","wgam"]:
                            den=ent.hist.Clone()
                            ibinMG=1
                            #for v in [1.0,1.2,1.1,0.67,0.78]:
                            for v in [1.0,1.08,1.05,0.78,0.83]:
                                den.SetBinContent(ibinMG,(v-1.0)*ent.hist.GetBinContent(ibinMG))
                                #den.SetBinError(ibinMG,v*ent.hist.GetBinError(ibinMG))
                                den.SetBinError(ibinMG,0.0)
                                ibinMG+=1
                            mg_den_tmp.Add(den,1.0)
                    self.ratioMG.Divide(mg_den_tmp)
                if options.getMJNF:
                    multijethist = self.bkgs['dqcd'].hist
                    for myMJBin in range(1,multijethist.GetNbinsX()+1):
                        data_mj = self.data.hist.GetBinContent(myMJBin)
                        totalbkgmj = self.bkg_sum.GetBinContent(myMJBin)
                        mjinBin = multijethist.GetBinContent(myMJBin)
                        nfmjbin=1.0
                        if mjinBin>0.0:
                            nfmjbin = (data_mj - (totalbkgmj - mjinBin))/mjinBin
                        print 'multijethist: ',myMJBin,' MJ: ',multijethist.GetBinContent(myMJBin),' NF: ',nfmjbin
                    
                # compute the mu-error
                if options.blind and not options.ph_ana:
                    leftToRight=1
                    CUTRANGE = range(0,self.signif.GetNbinsX()+1)
                    if 'LtoRCut' in getHistPars(self.name):
                        leftToRight = getHistPars(self.name)['LtoRCut']
                    for ibinA in CUTRANGE:
                        ibin = ibinA
                        if leftToRight==0:
                            ibin = self.signif.GetNbinsX() - ibinA
                        #print ibin
                        cut_Nsig = self.sign.hist.Integral(0,ibin)
                        cut_Nbkg = self.bkg_sum.Integral(0,ibin)
                        cut_NsigOpp=0.0
                        cut_NbkgOpp=0.0
                        if leftToRight==0:
                            cut_Nsig = self.sign.hist.Integral(ibin,10001)
                            cut_Nbkg = self.bkg_sum.Integral(ibin,10001)
                        elif leftToRight==2: # do this bin-by-bin
                            cut_Nsig = self.sign.hist.Integral(ibin,ibin)
                            cut_Nbkg = self.bkg_sum.Integral(ibin,ibin)
                        elif leftToRight==3: # add bins together
                            cut_NsigOpp = self.sign.hist.Integral(ibin+1,10001)
                            cut_NbkgOpp = self.bkg_sum.Integral(ibin+1,10001)
                        elif (leftToRight==4 and ibin%2==0): # pair every 2 bins together
                            cut_Nsig = self.sign.hist.GetBinContent(ibin)
                            cut_Nbkg = self.bkg_sum.GetBinContent(ibin)
                            if ibin!=0 and ibin!=2: #0 included in CUTRANGE but not in actual histograms - binning starts at 1
                                cut_NsigOpp = self.sign.hist.GetBinContent(ibin)
                                cut_NbkgOpp = self.bkg_sum.GetBinContent(ibin)
                                cut_Nsig = self.sign.hist.GetBinContent(ibin-1)
                                cut_Nbkg = self.bkg_sum.GetBinContent(ibin-1)
                        elif (leftToRight==4 and ibin%2==1): # pair every 2 bins together
                            if ibin!=1:
                                cut_NsigOpp = self.sign.hist.GetBinContent(ibin+1)
                                cut_NbkgOpp = self.bkg_sum.GetBinContent(ibin+1)
                                cut_Nsig = self.sign.hist.GetBinContent(ibin)
                                cut_Nbkg = self.bkg_sum.GetBinContent(ibin)
                        #else:
                        #    cut_Nsig = self.sign.hist.Integral(ibin,ibin)
                        #    cut_Nbkg = self.bkg_sum.Integral(ibin,ibin)

                        #print 'cut_Nbkg: ',cut_Nbkg,' ',cut_Nsig
                        if cut_Nsig>0.0 and cut_Nbkg>0.0:
                            signifV = 2.0*math.sqrt(cut_Nbkg)/cut_Nsig
                            if cut_NsigOpp>0.0:
                                signifVOpp = 2.0*math.sqrt(cut_NbkgOpp)/cut_NsigOpp
                                if  (leftToRight==3 or leftToRight==4) and signifV>0.0 and signifVOpp>0.0: # add bins together
                                    signifV = 1./math.sqrt(1./signifV**2+1./signifVOpp**2)
                            self.signif.SetBinContent(ibin, signifV)

                            wBKG=0.0
                            madgraph=''
                            if options.madgraph:
                                madgraph='Mad'
                            if ('wqcd'+madgraph) in self.bkgs and 'wewk' in self.bkgs:
                                wBKG = self.bkgs['wqcd'+madgraph].hist.Integral(0,ibin)+self.bkgs['wewk'].hist.Integral(0,ibin)
                                wBKGOpp=0.0
                                if leftToRight==0:
                                    wBKG = self.bkgs['wqcd'+madgraph].hist.Integral(ibin,10001)+self.bkgs['wewk'].hist.Integral(ibin,10001)
                                elif leftToRight==2:
                                    wBKG = self.bkgs['wqcd'+madgraph].hist.Integral(ibin,ibin)+self.bkgs['wewk'].hist.Integral(ibin,ibin)
                                elif leftToRight==3: # add bins together
                                    wBKGOpp = self.bkgs['wqcd'+madgraph].hist.Integral(ibin+1,10001)+self.bkgs['wewk'].hist.Integral(ibin+1,10001)
                                elif leftToRight==4 and ibin%2==0:# pair every 2 bins together
                                    wBKG = self.bkgs['wqcd'+madgraph].hist.GetBinContent(ibin-1)+self.bkgs['wewk'].hist.GetBinContent(ibin-1)
                                    wBKGOpp = self.bkgs['wqcd'+madgraph].hist.GetBinContent(ibin)+self.bkgs['wewk'].hist.GetBinContent(ibin)
                                    if ibin==0 or ibin==2:#For leading Nominal bin (unpaired)
                                        wBKG = self.bkgs['wqcd'+madgraph].hist.Integral(ibin,ibin)+self.bkgs['wewk'].hist.Integral(ibin,ibin)
                                elif leftToRight==4 and ibin%2==1:# pair every 2 bins together
                                    wBKG = self.bkgs['wqcd'+madgraph].hist.GetBinContent(ibin)+self.bkgs['wewk'].hist.GetBinContent(ibin)
                                    wBKGOpp = self.bkgs['wqcd'+madgraph].hist.GetBinContent(ibin+1)+self.bkgs['wewk'].hist.GetBinContent(ibin+1)
                                    if ibin==1:#For leading Nominal bin (unpaired)
                                        wBKG = self.bkgs['wqcd'+madgraph].hist.Integral(ibin,ibin)+self.bkgs['wewk'].hist.Integral(ibin,ibin)

                            if ('zqcd'+madgraph) in self.bkgs and 'zewk' in self.bkgs:
                                zBKG = self.bkgs['zqcd'+madgraph].hist.Integral(0,ibin)+self.bkgs['zewk'].hist.Integral(0,ibin)
                                zBKGOpp=0.0
                                if leftToRight==0:
                                    zBKG = self.bkgs['zqcd'+madgraph].hist.Integral(ibin,10001)+self.bkgs['zewk'].hist.Integral(ibin,10001)
                                elif leftToRight==2:
                                    zBKG = self.bkgs['zqcd'+madgraph].hist.Integral(ibin,ibin)+self.bkgs['zewk'].hist.Integral(ibin,ibin)
                                elif leftToRight==3: # add bins together
                                    zBKGOpp = self.bkgs['zqcd'+madgraph].hist.Integral(ibin+1,10001)+self.bkgs['zewk'].hist.Integral(ibin+1,10001)
                                elif leftToRight==4 and ibin%2==0:# pair every 2 bins together
                                    zBKG = self.bkgs['zqcd'+madgraph].hist.GetBinContent(ibin-1)+self.bkgs['zewk'].hist.GetBinContent(ibin-1)
                                    zBKGOpp = self.bkgs['zqcd'+madgraph].hist.GetBinContent(ibin)+self.bkgs['zewk'].hist.GetBinContent(ibin)
                                    if ibin==2:#For leading Nominal bin (unpaired)
                                        zBKG = self.bkgs['zqcd'+madgraph].hist.Integral(ibin,ibin)+self.bkgs['zewk'].hist.Integral(ibin,ibin)
                                elif leftToRight==4 and ibin%2==1:# pair every 2 bins together
                                    zBKG = self.bkgs['zqcd'+madgraph].hist.GetBinContent(ibin)+self.bkgs['zewk'].hist.GetBinContent(ibin)
                                    zBKGOpp = self.bkgs['zqcd'+madgraph].hist.GetBinContent(ibin+1)+self.bkgs['zewk'].hist.GetBinContent(ibin+1)
                                    if ibin==1:#For leading Nominal bin (unpaired)
                                        zBKG = self.bkgs['zqcd'+madgraph].hist.Integral(ibin,ibin)+self.bkgs['zewk'].hist.Integral(ibin,ibin)
                                total_zcr=-100.0
                                total_zcrOpp=-100.0
                                if self.zcr_stack and not self.zcr_stack.bkg_sum:
                                    self.zcr_stack.bkg_sum = self.zcr_stack.GetTotalBkgHist()
                                total_zcr = self.zcr_stack.bkg_sum.Integral(0,ibin)
                                if leftToRight==0 and self.zcr_stack:
                                    total_zcr = self.zcr_stack.bkg_sum.Integral(ibin,10001)
                                elif (leftToRight==2) and self.zcr_stack:
                                    total_zcr = self.zcr_stack.bkg_sum.GetBinContent(ibin)
                                elif leftToRight==3: # add bins together
                                    total_zcrOpp = self.zcr_stack.bkg_sum.Integral(ibin+1,10001)
                                elif leftToRight==4 and ibin%2==0:# pair every 2 bins together
                                    total_zcr = self.zcr_stack.bkg_sum.GetBinContent(ibin-1)
                                    total_zcrOpp = self.zcr_stack.bkg_sum.GetBinContent(ibin)
                                    if ibin==2:#For leading Nominal bin (unpaired)
                                        total_zcr = self.zcr_stack.bkg_sum.Integral(ibin,ibin)
                                elif leftToRight==4 and ibin%2==1:# pair every 2 bins together
                                    total_zcr = self.zcr_stack.bkg_sum.GetBinContent(ibin)
                                    total_zcrOpp = self.zcr_stack.bkg_sum.GetBinContent(ibin+1)
                                    if ibin==1:#For leading Nominal bin (unpaired)
                                        total_zcr = self.zcr_stack.bkg_sum.Integral(ibin,ibin)
                                if total_zcr>0.0:
                                    total_zcr = 1.0/math.sqrt(total_zcr)
                                if total_zcrOpp>0.0:
                                    total_zcrOpp = 1.0/math.sqrt(total_zcrOpp)
                                #print ibin,cut_Nbkg,total_zcr,zBKG,wBKG,cut_Nsig,(2.0*math.sqrt(cut_Nbkg + (zBKG*total_zcr)**2 +(wBKG*0.015)**2 )/cut_Nsig)
                                signifVal = 2.0*math.sqrt(cut_Nbkg + (zBKG*total_zcr)**2 +(wBKG*0.015)**2 )/cut_Nsig
                                if leftToRight==3 or leftToRight==4: # add bins together
                                    signifValOpp=0.0
                                    if cut_NsigOpp>0.0:
                                        signifValOpp = 2.0*math.sqrt(cut_NbkgOpp + (zBKGOpp*total_zcrOpp)**2 +(wBKGOpp*0.015)**2 )/cut_NsigOpp
                                    if signifValOpp>0.0 and signifVal>0:
                                        signifVal = 1./math.sqrt(1./signifValOpp**2+1./signifVal**2)
                                    elif signifValOpp>0.0 and not signifVal>0:
                                        signifVal=signifValOpp
                                #print signifVal
                                #signifVal=4.*total_zcr/cut_Nbkg
                                #print signifVal,cut_Nbkg,total_zcr
                                self.signifCR.SetBinContent(ibin, signifVal)

            # Set Names
            pars = getHistPars(self.name)
            if 'xtitle' in pars and self.bkg_sum.GetXaxis() != None:
                self.ratio.GetXaxis().SetTitle(pars['xtitle'])
            if options.blind:
                self.ratio.GetYaxis().SetTitle('Sig./Bkg ')
            else:
                self.ratio.GetYaxis().SetTitle('Data / Bkg ')
            #if options.blind:
            #    for i in range(0,self.ratio.GetNbinsX()+1):
            #        self.ratio.SetBinError(i,0.0)
            #        self.ratio.SetBinContent(i,0.0)

            # Setting the size of ratio font
            bx = self.ratio.GetXaxis();
            by = self.ratio.GetYaxis();
            if not options.blind:
                self.ratio.SetMarkerSize(1.2);
                self.ratio.SetMarkerStyle(20);
                self.ratioMG.SetMarkerSize(0.6);
                self.ratioMG.SetMarkerStyle(22);                
            else:
                self.ratio.SetLineStyle(1);
                self.ratio.SetMarkerSize(0.05);
                self.signif.SetLineStyle(1);
                self.signif.SetMarkerSize(0.05);
                self.signif.SetLineColor(2);
                self.signif.SetMarkerColor(2);
                self.signif.SetLineWidth(2);
                self.signifCR.SetLineStyle(1);
                self.signifCR.SetMarkerSize(0.05);
                self.signifCR.SetLineColor(3);
                self.signifCR.SetMarkerColor(3);
                self.signifCR.SetLineWidth(2);

            self.ratio.SetLineColor(ROOT.kBlack);
            self.ratio.SetLineWidth(2);
            self.ratioMG.SetLineColor(ROOT.kMagenta);
            self.ratioMG.SetMarkerColor(ROOT.kMagenta);
            self.ratioMG.SetLineWidth(2);            

            #print 'Y:',ROOT.gStyle.GetTitleY();
            #ROOT.gStyle.SetTitleY(0.5);
            bx.SetTitleSize(ROOT.gStyle.GetTitleSize("x") * ratioPadScaling);
            bx.SetLabelSize(ROOT.gStyle.GetLabelSize("x") * ratioPadScaling);
            by.SetTitleSize(ROOT.gStyle.GetTitleSize("y") * ratioPadScaling);
            #by.SetTitleOffset(ROOT.gStyle.GetTitleOffset("y") / ratioPadScaling  );
            by.SetTitleOffset(ROOT.gStyle.GetTitleOffset("y") / ratioPadScaling  );
            #by.	CenterTitle(True);
            by.SetLabelSize(ROOT.gStyle.GetLabelSize("y") * ratioPadScaling);
            bx.SetTickLength(ROOT.gStyle.GetTickLength() * ratioPadScaling);

            #bx.SetTitle("Observable");
            #bx.SetTitle("Data/Bkg");
            bx.SetLabelSize(0.13);
            bx.SetLabelOffset(0.02);
            bx.SetTitleSize(0.14);
            bx.SetTitleOffset(1.2);

            #by.SetRangeUser(0.501, 1.499);
            #by.SetRangeUser(0.751, 1.249);
            by.SetRangeUser(0.601, 1.399);
            if options.ph_ana:
                by.SetRangeUser(0.501, 1.499);
            if options.blind:
                by.SetRangeUser(0,0.799);
                by.SetRangeUser(0,1.7999);
            by.SetLabelSize(0.13);
            by.SetLabelOffset(0.0125);
            by.SetTitleSize(0.14);
            by.SetTitleOffset(0.5);
            by.SetNdivisions(5);

            self.ratio.DrawCopy()

            #
            # Draw ratio error band
            #
            self.error_map['bkg_ratio'] = syst_ratio.Clone()
            #self.error_map['bkg_ratio'].SetFillStyle(3354)
            self.error_map['bkg_ratio'].SetFillStyle(3345) # 3004
            self.error_map['bkg_ratio'].SetFillColor(ROOT.kBlack)
            self.error_map['bkg_ratio'].SetMarkerColor(1)
            self.error_map['bkg_ratio'].SetMarkerSize(0)
            self.error_map['bkg_ratio'].SetLineColor(1)
            self.error_map['bkg_ratio'].Draw('SAME E2')
            # JES error ratio
            if syst_jes_ratio:
                self.error_map['syst_jes_ratio'] = syst_jes_ratio.Clone()
                self.error_map['syst_jes_ratio'].SetFillColor(0)
                self.error_map['syst_jes_ratio'].SetLineColor(3)
                self.error_map['syst_jes_ratio'].SetLineWidth(2)
                self.error_map['syst_jes_ratio'].SetMarkerColor(3)
                self.error_map['syst_jes_ratio'].SetLineStyle(1)
                self.error_map['syst_jes_ratio'].Draw('SAME E1') #HIST

            # Overlay the ratio plot on top of errors
            if options.blind:
                self.ratio.Draw('same hist')
                self.signif.Draw('same hist')
                self.signifCR.GetYaxis().SetRangeUser(0.0,1.5);
                self.signifCR.Draw('hist same')
                self.legr.Clear()
                self.legr.AddEntry(self.ratio,'S/B')
                self.legr.AddEntry(self.signif,'#sigma_{#mu} Stat 95% CL')
                self.legr.AddEntry(self.signifCR,'#sigma_{#mu} w/ZCR 95% CL')
                self.legr.Draw()
                optv=0.0
                for i in range(0,self.signifCR.GetNbinsX()+1):
                    print 'Bin:',i,self.signifCR.GetBinContent(i)
                    if abs(self.signifCR.GetNbinsX()+1 - i )<4:
                        if optv>0.0 and self.signifCR.GetBinContent(i)>0.0:
                            optv=1./math.sqrt((1./optv**2+(1./self.signifCR.GetBinContent(i))**2))
                        elif self.signifCR.GetBinContent(i)>0.0:
                            optv=self.signifCR.GetBinContent(i)
                print 'combine last 3 bins: ',optv

            else:
                self.ratio.Draw('same')
                if options.mg_ratio:
                    self.ratioMG.Draw('same hist')
                    self.legr.Clear()
                    self.legr.AddEntry(self.ratio,'Data/Sherpa228')
                    self.legr.AddEntry(self.ratioMG,'Data/MG FxFx')
                    self.legr.Draw()
            self.pads[ipad].RedrawAxis()
            self.pads[ipad].Update()

        # Draw a vertical line. If this option is set, it gets set to an x-coordinate.
        if options.vertical_line is not None:
            # How do we figure this out? TODO: fix...
            line_ymin = self.data.hist.GetYaxis().GetBinLowEdge(1)
            line_ymax = self.data.hist.GetMaximum() * 1.75
            # Draw the line.
            self.vline = ROOT.TLine(options.vertical_line, line_ymin, options.vertical_line, line_ymax)
            self.vline.SetLineStyle(9)
            self.vline.SetLineWidth(3)
            self.vline.SetLineColor(ROOT.kBlue)
            self.vline.Draw("same")
            log.info('Drawing vertical line at x = ' + str(options.vertical_line))

    #-----------------------------
    def SystBand(self, hists=[], syst=None, syst_ratio=None, linestyle=0, tot_bkg=None,other_syst=None):

        if len(hists)<2:
            log.info('MvaPlot - ERROR plot_syst_err_band does not have enough histograms to compute uncertainity: %s' %(len(hists)))

        # Draw
        nom=None
        nom = self.bkg_sum.Clone()

        for i in range(0,self.bkg_sum.GetNbinsX()+1):
            syst.SetPointEXhigh(i-1,self.bkg_sum.GetXaxis().GetBinWidth(i)/2.0)
            syst.SetPointEXlow(i-1,self.bkg_sum.GetXaxis().GetBinWidth(i)/2.0)
            # This REMOVES THE MC STAT uncertainty from the syst band
            if not options.show_mc_stat_err:
                syst.SetPointEYhigh(i-1,0.0)
                syst.SetPointEYlow(i-1,0.0)
            if other_syst:
                m=i
                e1=other_syst.GetErrorYhigh(m-1)
                e2=syst.GetErrorYhigh(m-1)
                new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                syst.SetPointEYhigh(m-1,new_e)
                e2=syst.GetErrorYlow(m-1)
                new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                syst.SetPointEYlow(m-1,new_e)

        if False:
            mysyst_jes = import_syst.systematics('JES', options.ph_ana)
            syst_jesr = syst.Clone()
            syst_jesr.SetName('syst_jesr')
        else:
            syst_jesr=None
        # iterate over the systematics
        for sys, ent in self.sys_bkgs.iteritems():
            if True:
                #if ent.hist.Integral()<3500.0:
                #print ent.hist.Integral(),' sys: ',sys,ent.hist.Integral(),' nom: ',nom.Integral()
                for m in range(1,nom.GetNbinsX()+1):
                    nom_val=nom.GetBinContent(m)
                    e1=(ent.hist.GetBinContent(m)-nom_val)
                    #print 'bin: ',m,' e1: ',e1,' nom_val: ',nom_val,' variation: ',ent.hist.GetBinContent(m),' ehig: ',syst.GetErrorYhigh(m-1),' elow: ',syst.GetErrorYlow(m-1)
                    #print 'stat error: ',nom.GetBinError(m),' asym: ',syst.GetErrorYhigh(m-1)
                    if e1>0:
                        e2=syst.GetErrorYhigh(m-1)
                        new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                        syst.SetPointEYhigh(m-1,new_e)
                    elif e1<0:
                        e2=syst.GetErrorYlow(m-1)
                        new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                        syst.SetPointEYlow(m-1,new_e)
                    # adding the jes systematics
                    if syst_jesr and sys in mysyst_jes.getsystematicsList():
                        if e1>0:
                            e2=syst_jesr.GetErrorYhigh(m-1)
                            new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                            syst_jesr.SetPointEYhigh(m-1,new_e)
                        elif e1<0:
                            e2=syst_jesr.GetErrorYlow(m-1)
                            new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                            syst_jesr.SetPointEYlow(m-1,new_e)
        #
        # Calculate the systematic band for a ratio plot
        #
        x1=ROOT.Double()
        y1=ROOT.Double()
        syst_jesr_ratio=None
        if syst_jesr:
            syst_jesr_ratio = syst_ratio.Clone()        
        for i in range(0,self.bkg_sum.GetNbinsX()+1):
            syst_ratio.SetPointEXhigh(i-1,self.bkg_sum.GetXaxis().GetBinWidth(i)/2.0)
            syst_ratio.SetPointEXlow(i-1,self.bkg_sum.GetXaxis().GetBinWidth(i)/2.0)
            if syst_jesr_ratio:
                syst_jesr_ratio.SetPointEXhigh(i-1,self.bkg_sum.GetXaxis().GetBinWidth(i)/2.0)
                syst_jesr_ratio.SetPointEXlow(i-1,self.bkg_sum.GetXaxis().GetBinWidth(i)/2.0)


        for j in range(1,tot_bkg.GetNbinsX()+1):
            # Set Y value to 1
            syst_ratio.GetPoint(j-1,x1,y1)
            syst_ratio.SetPoint(j-1,x1,1.0)
            if syst_jesr_ratio:
                syst_jesr_ratio.SetPoint(j-1,x1,1.0)
            val=tot_bkg.GetBinContent(j)
            if val==0.0:
                continue

            #
            # Normalize error
            #
            eyu=syst.GetErrorYhigh   (j-1)/val
            eyd=syst.GetErrorYlow    (j-1)/val
            syst_ratio.SetPointEYhigh(j-1,eyu)
            syst_ratio.SetPointEYlow (j-1,eyd)
            # JES
            if syst_jesr_ratio:
                eyu=syst_jesr.GetErrorYhigh   (j-1)/val
                eyd=syst_jesr.GetErrorYlow    (j-1)/val
                syst_jesr_ratio.SetPointEYhigh(j-1,eyu)
                syst_jesr_ratio.SetPointEYlow (j-1,eyd)
            #print 'err up: ',eyu,' down: ',eyd

        return syst_jesr_ratio

    def CreateStack(self):
        self.stack   = ROOT.THStack(self.name, self.name)
        self.bkg_sum = None

        for bkg in sorted(self.bkgs.keys(), key=getSampleSortKey):

            he = self.bkgs[bkg]
            self.stack.Add(he.hist)

            if self.bkg_sum == None:
                self.bkg_sum = he.hist.Clone()
                if options.draw_norm:
                    self.bkg_sum.SetFillColor  (219)
                    self.bkg_sum.SetMarkerColor(219)
                    self.bkg_sum.SetLineColor  (219)
            else:
                self.bkg_sum.Add(he.hist)

        if self.data != None and not options.blind:
            self.leg.AddEntry(self.data.hist,'Data')
            self.bkg_sum_altb=self.data.hist.Clone()
            self.bkg_sum_altb.SetLineColor(ROOT.kRed)
            self.bkg_sum_altb.SetMarkerColor(ROOT.kRed)
            self.bkg_sum_altb.SetMarkerSize(0)
            self.bkg_sum_altb.SetFillColor(1)
            #self.bkg_sum_altb.SetFillStyle(3005)
            self.bkg_sum_altb.SetFillStyle(3345) #3004
            self.bkg_sum_altb.SetLineColor(1)
            self.bkg_sum_altb.SetLineWidth(0)
            self.leg.AddEntry(self.bkg_sum_altb,'Uncertainty')

        for bkg in sorted(self.bkgs.keys(), key=getLabelSortKey):
            he = self.bkgs[bkg]
            if he.hist.Integral()==0:
                continue
            he.DrawHist(None, self.leg)

    #---------------------
    def UpdateStack(self):

        pars = getHistPars(self.name)

        if 'xtitle' in pars and self.stack.GetXaxis() != None:
            self.stack.GetXaxis().SetTitle(pars['xtitle'])

        if 'ytitle' in pars and self.stack.GetYaxis() != None:
            self.stack.GetYaxis().SetTitle(pars['ytitle'])

        ymax = self.GetYaxisMax()
        if ymax > 0.0:
            if self.IsLogy():
                self.stack.SetMaximum(25.0*ymax)
                self.stack.SetMinimum(0.1)
            else:
                self.stack.SetMaximum( 1.8*ymax)
                self.stack.SetMinimum(0.0)

        if 'ymin' in pars:
            self.stack.SetMinimum(pars['ymin'])
        elif options.ymin != None:
            self.stack.SetMinimum(options.ymin)
        if 'bin_labels' in pars:
            n=1
            for labeli in pars['bin_labels']:
                self.stack.GetXaxis().SetBinLabel(n,labeli)
                n+=1
        if 'ymax' in pars:
            self.stack.SetMaximum(pars['ymax'])
        elif options.ymax != None:
            self.stack.SetMaximum(options.ymax)
            pars['ymax']=options.ymax
        #else:
        #    ['ymax']=self.stack.GetMaximum()
        if options.do_logy:
            self.stack.SetMinimum(0.1)
        if 'xmax' in pars and 'xmin' in pars:
            self.stack.GetXaxis().SetRangeUser(pars['xmin'],pars['xmax'])
        elif 'xmin' in pars:
            self.stack.GetXaxis().SetRangeUser(pars['xmin'],1.0)
        elif 'xmax' in pars:
            self.stack.GetXaxis().SetRangeUser(0.0,pars['xmax'])
        elif options.xmax != None:
            self.stack.GetXaxis().SetRangeUser(options.xmin,options.xmax)
    #--------------------
    def UpdateHist(self, h, sample=None, ignore_max=False):

        pars = getHistPars(self.name)
        if 'xtitle' in pars and h.GetXaxis() != None:
            h.GetXaxis().SetTitle(pars['xtitle'])

        if 'ytitle' in pars and h.GetYaxis() != None:
            h.GetYaxis().SetTitle(pars['ytitle'])

        ymax=-1.0
        if not ignore_max:
            ymax = self.GetYaxisMax()
        if ymax > 0.0:
            if self.IsLogy():
                h.SetMaximum(5.0*ymax)
                h.SetMinimum(0.1)
            else:
                h.SetMaximum( 1.1*ymax)
                h.SetMinimum(0.0)

        if 'ymin' in pars:
            h.SetMinimum(pars['ymin'])
        elif options.ymin != None:
            h.SetMinimum(options.ymin)
        if 'bin_labels' in pars:
            n=1
            for labeli in pars['bin_labels']:
                h.GetXaxis().SetBinLabel(n,labeli)
                n+=1
        if 'ymax' in pars:
            h.SetMaximum(pars['ymax'])
        elif options.ymax != None:
            h.SetMaximum(options.ymax)

        if sample!=None:
            style = getStyle(sample)
            if 'line_width' in style:
                h.SetLineWidth(style['line_width'])
            if 'line_style' in style:
                h.SetLineStyle(style['line_style'])

        if 'xmax' in pars and 'xmin' in pars:
            h.GetXaxis().SetRangeUser(pars['xmin'],pars['xmax'])
        elif 'xmin' in pars:
            h.GetXaxis().SetRangeUser(pars['xmin'],1.0)
        elif 'xmax' in pars:
            h.GetXaxis().SetRangeUser(0.0,pars['xmax'])
        elif options.xmax != None:
            h.GetXaxis().SetRangeUser(options.xmin,options.xmax)

    #--------------------
    def GetYaxisMax(self):
        ymax = 0.0

        ymax = max([ymax, self.GetHistMax(self.data.hist)])
        ymax = max([ymax, self.GetHistMax(self.sign.hist)])

        if self.stack != None:
            ymax = max([ymax, self.stack.GetMaximum()])

        return ymax

    #---------------------------
    def GetHistMax(self, hist):
        ymax = None

        for ibin in range(1, hist.GetNbinsX()+1):
            val = hist.GetBinContent(ibin)
            err = hist.GetBinError  (ibin)

            if val > 0.0:
                if ymax == None:
                    ymax = val + err
                else:
                    ymax = max([ymax, val+err])

        return ymax

#---
def syst_names():

    syst_name_map={'jes_n':'JES Down',
                   'jvf_n':'JVF Down',
                   'jes_p':'JES Up',
                   'jvf_p':'JVF Up',
                   'qflip_p':'Charge Flip Up',
                   'qflip_n':'Charge Flip Down',
                   'ms_p':'Muon Scale Up',
                   'ms_n':'Muon Scale Down',
                   'mu_eff_p':'Muon Eff Up',
                   'mu_eff_n':'Muon Eff Down',
                   'tau_eff_n':'Tau Eff Down',
                   'tau_eff_p':'Tau Eff Up',
                   'el_eff_n':'Electron Eff Down',
                   'el_eff_p':'Electron Eff Up',
                   'ees_low_p': 'Electron Scale Low p_{T} Up',
                   'ees_low_n': 'Electron Scale Low p_{T} Down',
                   'btag_cj_p':'Btag Charm Up',
                   'btag_cj_n':'Btag Charm Down',
                   'btag_lj_n':'Btag Light Down',
                   'btag_lj_p':'Btag Light Up',
                   'btag_bj_n':'Btag Bottom Down',
                   'btag_bj_p':'Btag Bottom Up',
                    'scalest_p':'MET Scale Up',
                    'scalest_n':'MET Scale Down',
                    'resost':'MET Resolution',

                    'ees_z_p':'Electron Scale Up',
                    'ees_z_n':'Electron Scale Down',
                    'ees_mat_p':'Electron Material Up',
                    'ees_mat_n':'Electron Material Down',
                    'ees_ps_p':'Electron Presampler Up',
                    'ees_ps_n':'Electron Presampler Down',

                    'eer_p':'Electron Resolution Up',
                    'eer_n':'Electron Resolution Down',
                    'bch_up' : 'BCH Up',
                    'bch_dn' : 'BCH Down',

                   'jer':'JER',
                   'pileup_p':'Pileup Up',
                   'pileup_n':'Pileup Down',
                   'id_p':'Muon ID Resolution Up',
                   'id_n':'Muon ID Resolution Down',
                   'mu_fr_n':'ID Resolution Down',
                   'el_stat_fr_p':'Electron FR Stat Up',
                   'el_stat_fr_n':'Electron FR Stat Down',
                   'mu_stat_fr_p':'Muon FR Stat Up',
                   'mu_stat_fr_n':'Muon FR Stat Down',
                    'lep_corr_fr_p':'FR Closure Up',
                    'lep_corr_fr_n':'FR Closure Down',
                   }
    return syst_name_map

#-------------------------------------------------------------------------
def writeSystTex(table_name, stack):

    try:
        out = open(table_name+'.table','w')
    except:
        print 'table_name: ',table_name,' does not exist'


    out.write('\\resizebox{\\textwidth}{!} { \n')
    out.write('\\begin{tabular}{l||llll|l}\n')
    out.write('\\hline\\hline\n')

    syst_name_map=syst_names()

    bkg_herr =  stack.sys_bkgs
    deleteme,hnom = stack.GetErrorHists()
    nom_err=ROOT.Double(0.0)
    nom_val = hnom.IntegralAndError(0,2001,nom_err)
    systs=[]
    total_uncer_up=0.0
    total_uncer_down=0.0
    for sys, ent in bkg_herr.iteritems():
        if nom_val<=0.0:
            nom_val=1.0
        my_ratio=(ent.hist.Integral(0,1001)-nom_val)/nom_val
        print sys,' ',ent.hist.Integral(0,1001),' nom: ',nom_val,' frac: ',my_ratio
        sys_name = sys
        if sys in syst_name_map:
            sys_name=syst_name_map[sys]
        systs+=[[sys_name,my_ratio]]
        if my_ratio>0.0:
            total_uncer_up+=my_ratio*my_ratio
        else:
            total_uncer_down+=my_ratio*my_ratio

    # Sort systematics
    for i in range(0,len(systs)):

        for j in range(i+1,len(systs)):
            if systs[i][1]*systs[i][1]<systs[j][1]*systs[j][1]:
                tmp=systs[i]
                systs[i]=systs[j]
                systs[j]=tmp

    my_order=mysyst.getsystematicsListWithDown()
    if options.syst_type!='All':
        my_order=mysyst.getsystematicsList()+symm_list
    if True:
        for key in my_order:
            for s in systs:
                #print s
                tmp_key=''
                for kk,ll in syst_name_map.iteritems():
                    if s[0]==ll:
                        tmp_key=kk
                        break
                if s[0]==key or key==tmp_key:
                    my_space=''
                    for nnn in range(0,25-len(s[0])):
                        my_space+=' '
                    line= s[0]+my_space+' & '+'%0.4f \\\\' %(s[1])
                    #line=' & '+'%0.4f ' %(s[1])
                    out.write('%s\n' %line)
    else:

        for s in systs:
            #print '"%s",' %s[0]
            my_space=''
            for nnn in range(0,25-len(s[0])):
                my_space+=' '
            line= s[0]+my_space+' & '+'%0.4f \\\\' %(s[1])
            #line= s[0]
            #line='%s & '+'%0.4f ' %(s[0],s[1])
            out.write('%s\n' %line)
    # Print errors
    my_err_up=math.sqrt(total_uncer_up)
    my_err_dw=math.sqrt(total_uncer_down)
    syst_err_up=my_err_up*nom_val
    syst_err_dw=my_err_dw*nom_val
    data_val= stack.data.hist.Integral(0,1001)
    data_err = math.sqrt(data_val)

    out.write('Total Uncertainty & $\\pm_{%0.4f}^{%0.4f}$ \\\\ ' %(my_err_dw,my_err_up))
    out.write('\\hline \\hline\n')
    out.write('Total Bkg & %0.2f $\\pm$ %0.2f (stat)$\\pm_{%0.2f}^{%0.2f}$ (syst) \\\\ \n' %(nom_val,nom_err,syst_err_dw,syst_err_up))
    out.write('Observed & %0.0f $\\pm$ %0.2f \\\\ \n' %(data_val,data_err))
    out.write('\\end{tabular}\n')
    out.write('}\n')
    out.close()

#-------------------------------------------------------------------------
def main():

    if len(args) != 1:
        log.error('Need exactly one input argument: %s' %str(args))
        sys.exit(1)

    #if options.blind:
    #    options.do_ratio=False
    #    log.info('Ratio turned off because histogram is blinded!')

    rpath = args[0]

    if not os.path.isfile(rpath):
        log.error('Input argument is not a valid file: %s' %rpath)
        sys.exit(1)

    if options.selkey == None:
        log.error('Missing required option: --selkey=<directory name>')
        sys.exit(1)

    rfile  = ROOT.TFile(rpath, 'READ')

    sfiles={}
    my_order=mysyst.getsystematicsListWithDown()
    if options.syst_type!='All':
        my_order=mysyst.getsystematicsList()+symm_list
    print 'Reading nSyst: ',len(my_order)
    for ia in my_order:
        sfiles[ia]=rfile

    #-----------------------------------------------------------------------------------------
    # automatically set the lumi for the 2017 and 2018
    if options.year==2018 and options.int_lumi==36207.66:
        options.int_lumi=58450.1
    if options.year==2017 and options.int_lumi==36207.66:
        options.int_lumi=44307.4

    #
    # Select histograms and samples for stacks
    #
    #bkgs = ['zewk', 'zqcd','wewk','wqcd','top1','top2']
    if options.madgraph:
        bkgs = ['zewk', 'zqcdMad','wewk','wqcdMad','tall','dqcd'] #,'zldy'
    else:
        bkgs = ['zewk', 'zqcd','wewk','wqcd','tall','dqcd'] #,'mqcd','zldy','vvv','susy'
        #bkgs = ['zewk', 'zqcd','wewk','wqcd','top2','vvv','dqcd'] #,'mqcd','zldy','vvv'
        if options.ph_ana:
            #bkgs = ['ttg', 'zgam','wgam','pho','zgamewk','wgamewk','zewk', 'zqcd','wewk','wqcd','tall'] #,'mqcd','zldy','vvv'
            bkgs = [ 'zgam','wgam','pho','zgamewk','wgamewk','tall','efakeph','jfakeph'] #,'mqcd','zldy','vvv', 'ttg',
    if options.add_fakeE and not options.ph_ana:
        bkgs+=['tth']
    if options.add_fakeE and options.ph_ana:
        bkgs+=['vbfg']
    if options.stack_signal:
        if not options.signal in bkgs: bkgs+=[options.signal]

    # Signal events to extract
    extract_sig=[]
    if options.extract_sig!=None:
        extract_sig = options.extract_sig.split(',')

    vars = ['mll', 'ptll', 'pttot', 'mt', 'dphill', 'outbdt', 'outknn']
    nf_map={}
    if options.sf_file!=None:
        sf_file=open(options.sf_file,'r')
        for l in sf_file:
            sfs1=l.split(' ')
            try:
                if sfs1[0].strip()=='top':
                    nf_map['top2']=float(sfs1[1].strip())
                    nf_map['top1']=float(sfs1[1].strip())
                elif sfs1[0].strip()=='z' or sfs1[0].strip()=='zSF' or sfs1[0].strip()=='zOF':
                    nf_map['zjet']=float(sfs1[1].strip())
                else: nf_map[sfs1[0].strip()]=float(sfs1[1].rstrip('\n').strip())
            except:  print 'Could not read: ',sfs1
        log.info('NF map: %s' %nf_map)
        sf_file.close()

    if options.vars != None:
        vars = options.vars.split(',')

    #config.setPlotDefaults(ROOT)
    Style()
    ROOT.gStyle.SetHatchesLineWidth(1)
    can = ROOT.TCanvas('stack', 'stack', *options.canvas_size)
    can.Draw()
    can.cd()

    stacks = []

    for var in vars:

        stack = DrawStack(var, rfile, options.signal, 'data', bkgs, nf_map, extract_sig, extrasignal=options.extrasignal)
        print 'nSYST: ',len(sfiles)
        if options.draw_syst:
            if len(sfiles)>0:
                stack.ReadSystFiles(sfiles)

        stack.Draw(can)
        stacks += [stack]

        if options.syst == 'SysAll':
            cname='%s_%s_Nominal' %(getSelKeyPath(), var)
        else:
            cname='%s_%s_%s' %(getSelKeyPath(), var, options.syst)

        updateCanvas(can, name=cname, data_hist=stack.data, bkg_sum_hist=stack.bkg_sum)

        if options.syst_see == 'allsyst':
            grouping=10
            syst_group = len(sfiles.keys())/grouping+1
            for i in range(0, syst_group):
                stack.PlotManySyst(sfiles.keys(), can, isSignal=True, groupStart=i*grouping, groupEnd=(i+1)*grouping)
                stack.PlotManySyst(sfiles.keys(), can, fillData=(not options.blind), groupStart=i*grouping, groupEnd=(i+1)*grouping)

        for syst in sorted(sfiles.keys()):
            if options.syst_see == 'all' or options.syst_see == syst:
                stack.PlotSystSig(syst, can)
                stack.PlotSystBkg(syst, can)

    if options.syst == 'SysAll' and options.make_syst_table:

        ROOT.gStyle.SetPadLeftMargin  (0.28)
        ROOT.gStyle.SetPadRightMargin (0.08)
        ROOT.gStyle.SetPadBottomMargin(0.10)

        can = ROOT.TCanvas('table', 'table', 600, 850)
        can.Draw()
        can.cd()

        for stack in stacks:
            stack.PlotSystTables(can)
    if options.syst_table:
        writeSystTex(options.syst_table, stack)

    # Delete Memory
    can.Clear()
    del stacks
    rfile.Close()
    del rfile
    return

###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":
    main()

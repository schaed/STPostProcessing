# Detail levels
DETAIL_LEVEL_JETS = 1
DETAIL_LEVEL_MET = 2

# these are variables to be read in. Note that vectors are read in through ReadEvent
myvars = [    ['jj_deta', '25', '0.0', '10.0'],
              ['jj_dphi', '32', '0.0', '3.2'],
              ['jj_mass', '70', '0.0', '7000.0'],
              ['trigger_lep', '2', '-0.5', '1.5'],
              ['n_jet', '10', '-0.5', '9.5'],
              ['n_bjet', '10', '-0.5', '9.5'],
              ['n_el', '4', '-0.5', '3.5'],
              ['n_mu', '4', '-0.5', '3.5'],
              ['n_ph', '4', '-0.5', '3.5'],
              #['n_ph_crackVetoCleaning', '4', '-0.5', '3.5'],
              ['n_baseel', '4', '-0.5', '3.5'],
              ['n_basemu', '4', '-0.5', '3.5'],
              ['n_mu_baseline_noOR', '4', '-0.5', '3.5'],
              ['n_mu_w', '4', '-0.5', '3.5'],
              ['n_el_w', '4', '-0.5', '3.5'],
              ['lep_trig_match', '2', '-0.5', '1.5'],
              ['met_tst_j1_dphi', '16', '0.0', '3.2'],
              ['met_tst_j2_dphi', '16', '0.0', '3.2'],
              ['met_tst_nolep_j1_dphi', '16', '0.0', '3.2'],
              ['met_tst_nolep_j2_dphi', '16', '0.0', '3.2'],
              ['met_soft_tst_et', '50', '0.0', '100.0'],
              ['met_soft_tst_sumet', '50', '0.0', '500.0'],
              ['met_tenacious_tst_et', '50', '0.0', '500.0'],
              ['met_tenacious_tst_nolep_et', '50', '0.0', '500.0'],
              ['met_tenacious_tst_nolep_phi', '5', '-3.2', '3.2'],
              ['met_tight_tst_et', '20', '0.0', '500.0'],
              #['met_tighter_tst_et', '100', '0.0', '500.0'],
              ['met_tenacious_tst_phi', '16', '0.0', '3.2'],
              ['met_tight_tst_phi', '16', '0.0', '3.2'],
              #['met_tighter_tst_phi', '32', '0.0', '3.2'],
              ['met_soft_tst_phi', '32', '0.0', '3.2'],
              ['met_cst_jet', '50', '0.0', '500.0'],
              #['truth_jj_mass', '70', '0.0', '7000.0'],
              #['truth_j2_pt', '25', '0.0', '500.0'],
              #['truth_jj_dphi', '16', '0.0', '3.2'],
              #['SherpaVTruthPt', '25', '0.0', '500.0'],              
              ['met_truth_et', '100', '0.0', '1000.0'],
              #['bcid', '100', '-0.5', '99.5'],
              #['BCIDDistanceFromFront', '100', '-0.5', '99.5'],
              ['averageIntPerXing', '20', '-0.5', '99.5'],
              #['lb', '100', '-0.5', '999.5'],
              ['n_vx', '20', '-0.5', '99.5'],
              ['tmva', '20', '-1.0', '1.0'],
#              ['vjWeight', '100', '0', '1.0'],
              ]
myvars_notplotted = [['trigger_met_encoded', '2', '0.0', '1.0'],
                         ['trigger_met_encodedv2', '2', '0.0', '1.0'],
              ['passVjetsFilter', '2', '0.0', '1.0'],
              ['passVjetsFilterTauEl', '2', '0.0', '1.0'],
              ['passVjetsPTV', '2', '0.0', '1.0'],
                         ['passJetCleanTight', '2', '-0.5', '1.5'],
        ]

# These MET variables are plotted too, but if DETAIL_LEVEL_MET
# is set on the command line, *only* the met vars are plotted.
metplots = [
              ['trigger_met', '2', '-0.5', '1.5'],
              ['met_tst_et', '50', '0.0', '500.0'],
              ['met_tst_phi', '32', '-3.2', '3.2'],
              ['met_tst_nolep_et', '50', '0.0', '500.0'],
              ['met_tst_nolep_phi', '32', '-3.2', '3.2'],
              ['met_significance', '20', '0.0', '20.0'],
              ['metsig_tst', '20', '0.0', '20.0']
           ]

# these are variables not stored, but that we want to plot
myplots = [
              ['jetPt0', '50', '0.0', '500.0'],
              ['jetPt1', '50', '0.0', '500.0'],
              ['jetEta0', '45', '-4.5', '4.5'],
              ['jetEta1', '45', '-4.5', '4.5'],
              ['jjg_mass', '70', '0.0', '7000.0'],
              ['j1g_dR', '20', '0.0', '8.0'],
              ['j2g_dR', '20', '0.0', '8.0'],
              ['j3g_dR', '20', '0.0', '8.0'],
              ['j0jvt', '48', '-0.2', '1.0'],
              ['j1jvt', '48', '-0.2', '1.0'],
              ['j0fjvt', '20', '0.0', '2.0'],
              ['j1fjvt', '20', '0.0', '2.0'],
              ['jetTrackWidth0', '10', '0.0', '1.0'],
              ['jetTrackWidth1', '10', '0.0', '1.0'],
              ['jetNTracks0', '10', '0.0', '40.0'],
              ['jetNTracks1', '10', '0.0', '40.0'],
              ['jetPartonTruthLabelID0', '28', '-5.0', '22.0'],
              ['jetPartonTruthLabelID1', '28', '-5.0', '22.0'],
              ['etaj0TimesEtaj1', '10', '-100.0', '100.0'],
              ['chanFlavor', '10', '-0.5', '9.5'],
              ['lepPt0', '50', '0.0', '500.0'],
              ['lepPt1', '50', '0.0', '500.0'],
              ['mll',  '40', '0.0', '200.0'],
              ['mlg',  '50', '0.0', '500.0'],
              ['ptll', '50', '0.0', '500.0'],
              ['mllg', '50', '0.0', '500.0'],
              ['ptllg','50', '0.0', '500.0'],
              ['mt',   '50', '0.0', '500.0'],
              ['mtlepgammet',   '50', '0.0', '500.0'],
              ['mtgammet',   '50', '0.0', '500.0'],
              ['n_jet_fwd', '6', '-0.5', '5.5'],
              ['n_jet_fwdj', '6', '-0.5', '5.5'],
              ['n_jet_fwdj30', '6', '-0.5', '5.5'],
              ['n_jet_fwdj40', '6', '-0.5', '5.5'],
              ['n_jet_fwdj50', '6', '-0.5', '5.5'],
              ['n_jet_cen', '6', '-0.5', '5.5'],
              ['n_jet_cenj', '6', '-0.5', '5.5'],
              ['n_jet_cenj30', '6', '-0.5', '5.5'],
              ['n_jet_cenj40', '6', '-0.5', '5.5'],
              ['n_jet_cenj50', '6', '-0.5', '5.5'],
              ['n_tau', '6', '-0.5', '5.5'],
              ['lepCh0', '3', '-1.5', '1.5'],
              ['lepCh1', '3', '-1.5', '1.5'],
              ['j0timing', '20', '-50.0', '50.0'],
              ['j1timing', '20', '-50.0', '50.0'],
              ['n_truth_tau', '4', '-0.5', '3.5'],
              ['FilterMet', '50', '0.0', '500.0'],
              ['met_truth_phi', '6', '0.0', '6.2'],
              ['truth_max_jj_mass', '50', '0.0', '5000.0'],
              ['truth_j1_pt', '25', '0.0', '500.0'],
              ['truth_jj_deta', '10', '0.0', '10.0'],
              ['truthJet1Pt', '50', '0.0', '150.0'],
              ['nTruthJetMatch', '5', '-0.5', '4.5'],
              ['jetPt3', '20', '0.0', '200.0'],
              ['avgCentrality', '25', '0.0', '1.0'],
              ['maxCentrality', '25', '0.0', '1.0'],
              ['avgmj3_over_mjj', '50', '0.0', '1.0'],
              ['maxmj3_over_mjj', '50', '0.0', '1.0'],
              ['phcentrality', '25', '0.0', '1.0'],
              ['Mtt', '50', '0.0', '250.0'],
              ['phPt', '50', '0.0', '250.0'],
              ['phEta', '15', '-2.5', '2.5'],
              ['met_tst_ph_dphi', '12', '0.0', '3.15'],
              ['met_tst_nolep_ph_dphi', '12', '0.0', '3.15'],
              ['met_tst_j3_dphi', '32', '0.0', '3.2'],
              ['met_tst_nolep_j3_dphi', '32', '0.0', '3.2'],
              ['max_j3_dr', '20', '0.0', '10.0'],
              ['met_cst_tst_sub', '40', '-100.0', '100.0'],
              ['met_cst_tst_ratio', '20', '0.0', '0.5'],
              #['tmva', '100', '-1.0', '1.0'],
    ]

# drawn with the detail plotting option
jetplots=[['bcidPos', '100', '-0.5', '99.5'],
              ['n_jet_fwd', '6', '-0.5', '5.5'],
              ['n_jet_fwdj', '6', '-0.5', '5.5'],
              ['n_jet_fwdj30', '6', '-0.5', '5.5'],
              ['n_jet_fwdj40', '6', '-0.5', '5.5'],
              ['n_jet_fwdj50', '6', '-0.5', '5.5'],
              ['n_jet_cen', '6', '-0.5', '5.5'],
              ['n_jet_cenj', '6', '-0.5', '5.5'],
              ['n_jet_cenj30', '6', '-0.5', '5.5'],
              ['n_jet_cenj40', '6', '-0.5', '5.5'],
              ['n_jet_cenj50', '6', '-0.5', '5.5'],
              ['jetPt0', '100', '0.0', '500.0'],
              ['jetPt1', '100', '0.0', '500.0'],
              ['jetEta0', '90', '-4.5', '4.5'],
              ['jetEta1', '90', '-4.5', '4.5'],
              ['j0jvt', '50', '-0.25', '1.0'],
              ['j1jvt', '50', '-0.25', '1.0'],
              ['j0fjvt', '50', '0.0', '2.0'],
              ['j1fjvt', '50', '0.0', '2.0'],
              ['jj_deta', '50', '0.0', '10.0'],
              ['jj_dphi', '32', '0.0', '3.2'],
              ['jj_mass', '50', '0.0', '5000.0'],
              ['nTruthJetMatch', '5', '-0.5', '4.5'],
              ['met_tst_et', '50', '0.0', '500.0'],
              ]
syst_filter_vars = ['met_soft_tst_phi',
                    'met_soft_tst_sumet',
                    'met_tight_tst_et',
                    'met_tight_tst_phi',
                    'met_tighter_tst_et',
                    'met_tighter_tst_phi',
                    'met_truth_et',
                    'met_tenacious_tst_et',
                    'met_tenacious_tst_phi',
                    'met_tenacious_tst_nolep_et',
                    'met_tenacious_tst_nolep_phi',
                    'Mtt',
                    'n_tau',
                    'n_truth_tau',
                    #'phcentrality',
                    #'met_tst_ph_dphi',
                    #'met_tst_j3_dphi',
                    'jetPartonTruthLabelID0',
                    'jetPartonTruthLabelID1',
                    'jetNTracks0',
                    'jetNTracks1',
                    'jetTrackWidth0',
                    'jetTrackWidth1',
                    'chanFlavor',
                    'n_jet_fwd',
                    'n_jet_fwdj',
                    'n_jet_cen',
                    'n_jet_cenj',                    
                    'n_jet_fwdj40',
                    'n_jet_cenj40',
                    'n_jet_fwdj50',
                    'n_jet_cenj50',
                    'truth_jj_deta',
                    'truthJet1Pt',
                    'truth_j1_pt',
                    'met_truth_phi',
                    'truth_max_jj_mass',
                    'jjg_mass',                    
                    'j1g_dR',
                    'j2g_dR',
                    'j3g_dR',
                    'lep_trig_match',
                    'truth_jj_mass',
                    'truth_j2_pt',
                    'truth_jj_dphi',
                    'lepCh0',
                    'lepCh1',
                    'max_j3_dr',
                    'nTruthJetMatch',
                    'avgmj3_over_mjj',
                    'max_j3_dr',
                    'met_cst_tst_sub',
                    'met_cst_tst_ratio',
                    'FilterMet',
                ]
syst_filter_vars_plots = syst_filter_vars + ['n_el',
                    'n_ph',
                    'n_mu',
                    'n_mu_w',
                    'n_el_w',
                    'n_bjet',
                    'j0jvt',
                    'j1jvt',
                    'j0fjvt',
                    'j1fjvt',
                    'j0timing',
                    'j1timing',
                    'trigger_lep',
                    'trigger_met',
                    'n_baseel',
                    'n_basemu',
                    'n_mu_baseline_noOR',
                    'met_tst_phi',
                    'avgCentrality',
                    'n_jet_fwdj30',
                    'n_jet_cenj30',
                    #'phPt',
                    #'phEta',
]
mev_vars = ['jj_mass',
            'met_tst_et',
            'met_tst_nolep_et',
            'met_tenacious_tst_et',
            'met_tenacious_tst_nolep_et',
            'met_tight_tst_et',
            'met_tighter_tst_et',
            'met_soft_tst_et',
            'met_soft_tst_sumet',
            'met_cst_jet',
            'met_truth_et',
            'SherpaVTruthPt',
                ]

def GetVarStr(entry=0, syst_name='Nominal', ph_ana=False, v41older=False):
    varstr = []
    all_vars = myvars+metplots+myvars_notplotted
    if ph_ana:
        all_vars+=[['in_vy_overlap', '2', '-0.5', '1.5']]
    if not v41older:
        all_vars+=[['ph_pointing_z', '100', '-200.0', '200.0']]
    for i in all_vars:
        skip=False
        if syst_name!='Nominal':
            for j in syst_filter_vars:
                if i[0]==j:
                    skip=True
                    break
        if skip:
            continue
        varstr  +=[i[entry]]
    return varstr

def GetPltStr(entry=0, syst_name='Nominal', DetailLvl=0, v41older=False):
    varstr = []
    allvars = []
    allvars += myplots
    allvars += metplots
    allvars += myvars
    if not v41older:
        allvars+=[['ph_pointing_z', '100', '-200.0', '200.0']]
        
    # Different plotting detail levels.
    if DetailLvl == DETAIL_LEVEL_JETS:
        allvars = jetplots
    if DetailLvl == DETAIL_LEVEL_MET:
        allvars = metplots

    for i in allvars:
        skip=False
        if syst_name!='Nominal':
            for j in syst_filter_vars_plots:
                if i[0]==j:
                    skip=True
                    break
        if skip:
            continue
        varstr  +=[i[entry]]
    return varstr

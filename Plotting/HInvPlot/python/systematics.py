class systematics(object):
    def __init__(self,mode, photon_ana=False,mjj_syst=False):
        self.photon_ana=photon_ana
        self.mjj_syst = mjj_syst
        
        # list the theory uncertainties that are wanted for ZEWK, WEWK, ZStrong, and WStrong
        # for the PTV systematics, the systematics are the same for ZEWK, WEWK, ZStrong, and WStrong.
        # Using the transfer factor method, the systematics list will be different for each of ZEWK, WEWK, ZStrong, and WStrong. 
        # These names need to be updated for the tranfer method. 
        # Currently this is all commented out. Uncomment to run these.
        self.systematicsZewkTheory = []
        if self.mjj_syst:
            self.systematicsZewkTheory = ["vjetsMjj_QCD_kQCD__1up", "vjetsMjj_QCD_kQCD__1down",
                                       "vjetsMjj_QCD_kPS__1up",  "vjetsMjj_QCD_kPS__1down",
                                       "vjetsMjj_QCD_kMix__1up", "vjetsMjj_QCD_kMix__1down",
                                       "vjetsMjj_QCD_kRew__1up", "vjetsMjj_QCD_kRew__1down",
				                        # EWK uncertainties
				                       "vjetsMjj_EWK_kQCD__1up", "vjetsMjj_EWK_kQCD__1down",
                                       "vjetsMjj_EWK_kPS__1up",  "vjetsMjj_EWK_kPS__1down",
                                       "vjetsMjj_EWK_kMix__1up", "vjetsMjj_EWK_kMix__1down",
                                       "vjetsMjj_EWK_kRew__1up", "vjetsMjj_EWK_kRew__1down",] 
        #self.systematicsZewkTheory = ['vjets_d1kappa_EW__1up','vjets_d1kappa_EW__1down',
        #                              'vjets_d2kappa_EW__1up','vjets_d2kappa_EW__1down',
        #                              'vjets_d3kappa_EW__1up','vjets_d3kappa_EW__1down',
        #                              'vjets_d1K_NNLO__1up','vjets_d1K_NNLO__1down',
        #                              'vjets_d2K_NNLO__1up','vjets_d2K_NNLO__1down',
        #                              'vjets_d3K_NNLO__1up','vjets_d3K_NNLO__1down',
        #                              'vjets_dK_NNLO_mix__1up','vjets_dK_NNLO_mix__1down',
        #                              'vjets_dK_PDF__1up','vjets_dK_PDF__1down',]
        self.systematicsWewkTheory = self.systematicsZewkTheory
        self.systematicsZstrongTheory = self.systematicsZewkTheory
        self.systematicsWstrongTheory = self.systematicsZewkTheory

        self.systematicsSignalPDF = ['ATLAS_PDF4LHC_NLO_30_alphaS__1up','ATLAS_PDF4LHC_NLO_30_alphaS__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV30__1up','ATLAS_PDF4LHC_NLO_30_EV29__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV28__1up','ATLAS_PDF4LHC_NLO_30_EV27__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV26__1up','ATLAS_PDF4LHC_NLO_30_EV25__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV24__1up','ATLAS_PDF4LHC_NLO_30_EV23__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV22__1up','ATLAS_PDF4LHC_NLO_30_EV21__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV20__1up','ATLAS_PDF4LHC_NLO_30_EV19__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV18__1up','ATLAS_PDF4LHC_NLO_30_EV17__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV16__1up','ATLAS_PDF4LHC_NLO_30_EV15__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV14__1up','ATLAS_PDF4LHC_NLO_30_EV13__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV12__1up','ATLAS_PDF4LHC_NLO_30_EV11__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV10__1up','ATLAS_PDF4LHC_NLO_30_EV9__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV8__1up','ATLAS_PDF4LHC_NLO_30_EV7__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV6__1up','ATLAS_PDF4LHC_NLO_30_EV5__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV4__1up','ATLAS_PDF4LHC_NLO_30_EV3__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV2__1up','ATLAS_PDF4LHC_NLO_30_EV1__1up',]
        self.systematicsGGFSignal =[#'ggF_gg2H_PSVarWeights__1up','ggF_gg2H_PSVarWeights__1down',
                                        "ggF_gg2H_mu__1up","ggF_gg2H_res__1up","ggF_gg2H_qm_t__1up",
                                         "ggF_gg2H_mig01__1up","ggF_gg2H_mig12__1up","ggF_gg2H_vbf2j__1up",
                                         "ggF_gg2H_vbf3j__1up","ggF_gg2H_pTH60__1up","ggF_gg2H_pTH120__1up"] 
        self.systematicsVBFSignal =['VBF_qqH_STJetVeto34__1up','VBF_qqH_STJetVeto34__1down',
                                    'VBF_qqH_MjjPSVarWeights__1up','VBF_qqH_MjjPSVarWeights__1down',
                                    'VBF_qqH_DphijjPSVarWeights__1up','VBF_qqH_DphijjPSVarWeights__1down',
                                    'VBF_qqH_25__1up','VBF_qqH_2jet__1up',
                                    'VBF_qqH_Mjj1500__1up','VBF_qqH_Mjj1000__1up',
                                    'VBF_qqH_Mjj700__1up','VBF_qqH_Mjj350__1up',
                                    'VBF_qqH_Mjj120__1up','VBF_qqH_Mjj60__1up',
                                    'VBF_qqH_200__1up','VBF_qqH_tot__1up',
                                    'nloEWKWeight__1up','nloEWKWeight__1down',
                                    'VBF_qqgamH_PSVar__1down','VBF_qqgamH_PSVar__1up',
                                     'VBF_qqgamH_Scale__1down','VBF_qqgamH_Scale__1up',] 
        
        self.systematicsListDown=["MET_SoftTrk_ResoParaDown", "MET_SoftTrk_ResoPerpDown",
                                      'JET_JER_EffectiveNP_1__1down', 'JET_JER_EffectiveNP_2__1down', 'JET_JER_EffectiveNP_3__1down', 'JET_JER_EffectiveNP_4__1down', 'JET_JER_EffectiveNP_5__1down', 'JET_JER_EffectiveNP_6__1down', 'JET_JER_EffectiveNP_7__1down', #'JET_JER_EffectiveNP_7restTerm__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV30__1down','ATLAS_PDF4LHC_NLO_30_EV29__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV28__1down','ATLAS_PDF4LHC_NLO_30_EV27__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV26__1down','ATLAS_PDF4LHC_NLO_30_EV25__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV24__1down','ATLAS_PDF4LHC_NLO_30_EV23__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV22__1down','ATLAS_PDF4LHC_NLO_30_EV21__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV20__1down','ATLAS_PDF4LHC_NLO_30_EV19__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV18__1down','ATLAS_PDF4LHC_NLO_30_EV17__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV16__1down','ATLAS_PDF4LHC_NLO_30_EV15__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV14__1down','ATLAS_PDF4LHC_NLO_30_EV13__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV12__1down','ATLAS_PDF4LHC_NLO_30_EV11__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV10__1down','ATLAS_PDF4LHC_NLO_30_EV9__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV8__1down','ATLAS_PDF4LHC_NLO_30_EV7__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV6__1down','ATLAS_PDF4LHC_NLO_30_EV5__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV4__1down','ATLAS_PDF4LHC_NLO_30_EV3__1down',
                                     'ATLAS_PDF4LHC_NLO_30_EV2__1down','ATLAS_PDF4LHC_NLO_30_EV1__1down',
                                    'VBF_qqH_25__1down','VBF_qqH_2jet__1down',
                                    'VBF_qqH_Mjj1500__1down','VBF_qqH_Mjj1000__1down',
                                    'VBF_qqH_Mjj700__1down','VBF_qqH_Mjj350__1down',
                                    'VBF_qqH_Mjj120__1down','VBF_qqH_Mjj60__1down',
                                    'VBF_qqH_200__1down','VBF_qqH_tot__1down',
                                     "ggF_gg2H_mu__1down","ggF_gg2H_res__1down","ggF_gg2H_qm_t__1down",
                                         "ggF_gg2H_mig01__1down","ggF_gg2H_mig12__1down","ggF_gg2H_vbf2j__1down",
                                         "ggF_gg2H_vbf3j__1down","ggF_gg2H_pTH60__1down","ggF_gg2H_pTH120__1down",
                                  # MJ unc
                                  'MJUnc__1down','MJClos2016__1down','MJClos2017__1down','MJClos2018__1down','MJClosHDPhi2016__1down','MJClosHDPhi2017__1down','MJClosHDPhi2018__1down',
                                     'MJClosLDPhi2016__1down','MJClosLDPhi2017__1down','MJClosLDPhi2018__1down'
                                      ]
        self.removeList=['TAUS_','PH_','JET_MassRes_','JET_Rtrk_','JET_Comb_','FT_EFF_','eleANTISFEL_EFF_Iso_','EFakePh','GJet','JetFakePh']#,'nloEWKWeight__1up','nloEWKWeight__1down','xeSFTrigWeight__1up','xeSFTrigWeight__1down']
        # Filter these uncertainties for photon analysis
        if self.photon_ana:
            self.removeList=['TAUS_','JET_MassRes_','JET_Rtrk_','JET_Comb_','FT_EFF_','eleANTISFEL_EFF_Iso_','MJ','vvUnc','ggF_gg2H_','PH_EFF_TRIGGER_Uncertainty','nloEWKWeight_','xeSFTrigWeight','VBF_qqH_','JET_QG_']#,'xeSFTrigWeight'],'',
            #self.removeList+=['PDF','JER','JET','MET','MUON_SCALE','EG_SCALE','MUON_SAGITTA','MUON_ID_','EG_RESOLUTION','MUON_MS']
        self.allowList=[]#'VBF_qqH_',"Nominal"] #['VBF_qqgamH']#'VBF_qqH_']
        self.systematicsList=""
        self.load(mode)

    def Filter(self, inList):
        # Filter out the unwanted systematics 
        systematicsList_tmp = []
        for s in inList:
            filtFound=False
            for filt in self.removeList:
                if s.find(filt)>-0.5:
                    print 'Systematic was filtered out: ',s
                    filtFound=True
                    break
            if len(self.allowList)>0:
                skipAllow=True
                for allow in self.allowList:
                    if s.find(allow)>-0.5:
                        skipAllow=False
                        break
                if skipAllow:
                    continue
            if not filtFound:
                systematicsList_tmp+=[s]
        return systematicsList_tmp
        
    def load(self,mode="All"):

        
        if mode == "All":
            self.systematicsList = ['Nominal',
                                        'EG_RESOLUTION_ALL__1down', 'EG_RESOLUTION_ALL__1up',
                                        'EG_SCALE_AF2__1down', 'EG_SCALE_AF2__1up',
                                        'EG_SCALE_ALL__1down', 'EG_SCALE_ALL__1up',
                                        'JET_Comb_Baseline_Kin__1down', 'JET_Comb_Baseline_Kin__1up',
                                        'JET_Comb_Modelling_Kin__1down', 'JET_Comb_Modelling_Kin__1up',
                                        'JET_Comb_TotalStat_Kin__1down', 'JET_Comb_TotalStat_Kin__1up',
                                        'JET_Comb_Tracking_Kin__1down', 'JET_Comb_Tracking_Kin__1up',
                                        'JET_EtaIntercalibration_NonClosure_highE__1down', 'JET_EtaIntercalibration_NonClosure_highE__1up',
                                        'JET_EtaIntercalibration_NonClosure_negEta__1down', 'JET_EtaIntercalibration_NonClosure_negEta__1up',
                                        'JET_EtaIntercalibration_NonClosure_posEta__1down', 'JET_EtaIntercalibration_NonClosure_posEta__1up',
                                        'JET_Flavor_Response__1down', 'JET_Flavor_Response__1up',
                                        'JET_GroupedNP_1__1down', 'JET_GroupedNP_1__1up',
                                        'JET_GroupedNP_2__1down', 'JET_GroupedNP_2__1up',
                                        'JET_GroupedNP_3__1down', 'JET_GroupedNP_3__1up',
                                        'JET_JER_DataVsMC__1up', 'JET_JER_EffectiveNP_1__1up',
                                        'JET_JER_EffectiveNP_2__1up', 'JET_JER_EffectiveNP_3__1up',
                                        'JET_JER_EffectiveNP_4__1up', 'JET_JER_EffectiveNP_5__1up',
                                        'JET_JER_EffectiveNP_6__1up', 'JET_JER_EffectiveNP_7restTerm__1up',
                                        'JET_MassRes_Hbb__1down', 'JET_MassRes_Hbb__1up',
                                        'JET_MassRes_Top__1down', 'JET_MassRes_Top__1up',
                                        'JET_MassRes_WZ__1down', 'JET_MassRes_WZ__1up',
                                        'JET_Rtrk_Baseline_Sub__1down', 'JET_Rtrk_Baseline_Sub__1up',
                                        'JET_Rtrk_Modelling_Sub__1down', 'JET_Rtrk_Modelling_Sub__1up',
                                        'JET_Rtrk_TotalStat_Sub__1down', 'JET_Rtrk_TotalStat_Sub__1up',
                                        'JET_Rtrk_Tracking_Sub__1down', 'JET_Rtrk_Tracking_Sub__1up',
                                        'MET_SoftTrk_ResoPara', 'MET_SoftTrk_ResoPerp',
                                        'MET_SoftTrk_ScaleDown', 'MET_SoftTrk_ScaleUp',
                                        'MUON_ID__1down', 'MUON_ID__1up', 'MUON_MS__1down', 'MUON_MS__1up',
                                        'MUON_SAGITTA_RESBIAS__1down', 'MUON_SAGITTA_RESBIAS__1up', 'MUON_SAGITTA_RHO__1down', 'MUON_SAGITTA_RHO__1up',
                                        'MUON_SCALE__1down', 'MUON_SCALE__1up',
                                        'FT_EFF_B_systematics__1down', 'FT_EFF_B_systematics__1up', 'FT_EFF_C_systematics__1down', 'FT_EFF_C_systematics__1up', 'FT_EFF_Light_systematics__1down', 'FT_EFF_Light_systematics__1up', 'FT_EFF_extrapolation__1down', 'FT_EFF_extrapolation__1up', 'FT_EFF_extrapolation_from_charm__1down', 'FT_EFF_extrapolation_from_charm__1up',
                                        'EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                        'EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                        'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                        'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                        'EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                        'eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                        'eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                        'JET_fJvtEfficiency__1down', 'JET_fJvtEfficiency__1up', 'JET_JvtEfficiency__1down', 'JET_JvtEfficiency__1up',
                                        'MUON_EFF_TrigStatUncertainty__1down', 'MUON_EFF_TrigStatUncertainty__1up', 'MUON_EFF_TrigSystUncertainty__1down',
                                        'MUON_EFF_TrigSystUncertainty__1up', 'MUON_EFF_BADMUON_SYS__1down', 'MUON_EFF_BADMUON_SYS__1up', 'MUON_EFF_ISO_STAT__1down', 'MUON_EFF_ISO_STAT__1up', 'MUON_EFF_ISO_SYS__1down', 'MUON_EFF_ISO_SYS__1up', 'MUON_EFF_RECO_STAT_LOWPT__1down', 'MUON_EFF_RECO_STAT_LOWPT__1up', 'MUON_EFF_RECO_STAT__1down', 'MUON_EFF_RECO_STAT__1up', 'MUON_EFF_RECO_SYS_LOWPT__1down', 'MUON_EFF_RECO_SYS_LOWPT__1up', 'MUON_EFF_RECO_SYS__1down', 'MUON_EFF_RECO_SYS__1up', 'MUON_EFF_TTVA_STAT__1down', 'MUON_EFF_TTVA_STAT__1up', 'MUON_EFF_TTVA_SYS__1down', 'MUON_EFF_TTVA_SYS__1up',
                                        'PRW_DATASF__1down', 'PRW_DATASF__1up','xeSFTrigWeight__1up','xeSFTrigWeight__1down',
                                        'puSyst2018Weight__1up','puSyst2018Weight__1down',
                                        'MJUnc__1up','MJClos2016__1up','MJClos2017__1up','MJClos2018__1up','MJClosHDPhi2016__1up','MJClosHDPhi2017__1up','MJClosHDPhi2018__1up',
                                     'MJClosLDPhi2016__1up','MJClosLDPhi2017__1up','MJClosLDPhi2018__1up', #MJ
                                                'vvUnc__1up',
                                                'vvUnc__1down'
            ]
            self.systematicsList = ['Nominal',
                                        'EG_RESOLUTION_ALL__1down','EG_RESOLUTION_ALL__1up','EG_SCALE_AF2__1down','EG_SCALE_AF2__1up','EG_SCALE_ALL__1down','EG_SCALE_ALL__1up',
                                        'EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                       'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                       'EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                       'JET_BJES_Response__1down','JET_BJES_Response__1up',
                                       'JET_EffectiveNP_Detector1__1down','JET_EffectiveNP_Detector1__1up','JET_EffectiveNP_Detector2__1down','JET_EffectiveNP_Detector2__1up',
                                       'JET_EffectiveNP_Mixed1__1down','JET_EffectiveNP_Mixed1__1up','JET_EffectiveNP_Mixed2__1down','JET_EffectiveNP_Mixed2__1up','JET_EffectiveNP_Mixed3__1down','JET_EffectiveNP_Mixed3__1up',
                                       'JET_EffectiveNP_Modelling1__1down','JET_EffectiveNP_Modelling1__1up','JET_EffectiveNP_Modelling2__1down','JET_EffectiveNP_Modelling2__1up','JET_EffectiveNP_Modelling3__1down','JET_EffectiveNP_Modelling3__1up','JET_EffectiveNP_Modelling4__1down','JET_EffectiveNP_Modelling4__1up',
                                       'JET_EffectiveNP_Statistical1__1down','JET_EffectiveNP_Statistical1__1up','JET_EffectiveNP_Statistical2__1down','JET_EffectiveNP_Statistical2__1up','JET_EffectiveNP_Statistical3__1down','JET_EffectiveNP_Statistical3__1up','JET_EffectiveNP_Statistical4__1down','JET_EffectiveNP_Statistical4__1up','JET_EffectiveNP_Statistical5__1down','JET_EffectiveNP_Statistical5__1up','JET_EffectiveNP_Statistical6__1down','JET_EffectiveNP_Statistical6__1up',
                                       'JET_EtaIntercalibration_Modelling__1down','JET_EtaIntercalibration_Modelling__1up','JET_EtaIntercalibration_NonClosure_highE__1down','JET_EtaIntercalibration_NonClosure_highE__1up','JET_EtaIntercalibration_NonClosure_negEta__1down','JET_EtaIntercalibration_NonClosure_negEta__1up','JET_EtaIntercalibration_NonClosure_posEta__1down','JET_EtaIntercalibration_NonClosure_posEta__1up','JET_EtaIntercalibration_TotalStat__1down','JET_EtaIntercalibration_TotalStat__1up',
                                       'JET_Flavor_Composition__1down','JET_Flavor_Composition__1up','JET_Flavor_Response__1down','JET_Flavor_Response__1up',
                                       'JET_JER_DataVsMC_MC16__1down','JET_JER_DataVsMC_MC16__1up',
                                    'JET_JER_EffectiveNP_1__1up',
                                    'JET_JER_EffectiveNP_2__1up',
                                    'JET_JER_EffectiveNP_3__1up',
                                    'JET_JER_EffectiveNP_4__1up',
                                    'JET_JER_EffectiveNP_5__1up',
                                    'JET_JER_EffectiveNP_6__1up',
                                    'JET_JER_EffectiveNP_7__1up',
                                        'JET_JER_EffectiveNP_8__1up','JET_JER_EffectiveNP_8__1down',
                                        'JET_JER_EffectiveNP_9__1up','JET_JER_EffectiveNP_9__1down',
                                        'JET_JER_EffectiveNP_10__1up','JET_JER_EffectiveNP_10__1down',
                                        'JET_JER_EffectiveNP_11__1up','JET_JER_EffectiveNP_11__1down',
                                        'JET_JER_EffectiveNP_12restTerm__1up','JET_JER_EffectiveNP_12restTerm__1down',
                                        #'JET_JER_EffectiveNP_7restTerm__1up',
                                       'JET_Pileup_OffsetMu__1down','JET_Pileup_OffsetMu__1up','JET_Pileup_OffsetNPV__1down','JET_Pileup_OffsetNPV__1up','JET_Pileup_PtTerm__1down','JET_Pileup_PtTerm__1up','JET_Pileup_RhoTopology__1down','JET_Pileup_RhoTopology__1up','JET_PunchThrough_MC16__1down','JET_PunchThrough_MC16__1up','JET_SingleParticle_HighPt__1down','JET_SingleParticle_HighPt__1up',
                                       'JET_fJvtEfficiency__1down','JET_fJvtEfficiency__1up','JET_JvtEfficiency__1down','JET_JvtEfficiency__1up',
                                       'MET_SoftTrk_ResoPara','MET_SoftTrk_ResoPerp','MET_SoftTrk_ScaleDown','MET_SoftTrk_ScaleUp',
                                       'MUON_EFF_BADMUON_SYS__1down','MUON_EFF_BADMUON_SYS__1up','MUON_EFF_ISO_STAT__1down','MUON_EFF_ISO_STAT__1up','MUON_EFF_ISO_SYS__1down','MUON_EFF_ISO_SYS__1up','MUON_EFF_RECO_STAT_LOWPT__1down','MUON_EFF_RECO_STAT_LOWPT__1up','MUON_EFF_RECO_STAT__1down','MUON_EFF_RECO_STAT__1up','MUON_EFF_RECO_SYS_LOWPT__1down','MUON_EFF_RECO_SYS_LOWPT__1up','MUON_EFF_RECO_SYS__1down','MUON_EFF_RECO_SYS__1up','MUON_EFF_TTVA_STAT__1down','MUON_EFF_TTVA_STAT__1up','MUON_EFF_TTVA_SYS__1down','MUON_EFF_TTVA_SYS__1up','MUON_EFF_TrigStatUncertainty__1down','MUON_EFF_TrigStatUncertainty__1up','MUON_EFF_TrigSystUncertainty__1down','MUON_EFF_TrigSystUncertainty__1up',
                                       'MUON_ID__1down','MUON_ID__1up','MUON_MS__1down','MUON_MS__1up','MUON_SAGITTA_RESBIAS__1down','MUON_SAGITTA_RESBIAS__1up','MUON_SAGITTA_RHO__1down','MUON_SAGITTA_RHO__1up','MUON_SCALE__1down','MUON_SCALE__1up',
                                       'PH_EFF_ID_Uncertainty__1down','PH_EFF_ID_Uncertainty__1up','PH_EFF_ISO_Uncertainty__1down','PH_EFF_ISO_Uncertainty__1up','PH_EFF_TRIGGER_Uncertainty__1down','PH_EFF_TRIGGER_Uncertainty__1up',
                                       'PRW_DATASF__1down','PRW_DATASF__1up',
                                       'xeSFTrigWeight__1up','xeSFTrigWeight__1down',
                                       'puSyst2018Weight__1up','puSyst2018Weight__1down',
                                        'eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up',
                                    'muoANTISFEL_EFF_ID__1down','muoANTISFEL_EFF_ID__1up',
    'MJUnc__1up','MJClos2016__1up','MJClos2017__1up','MJClos2018__1up','MJClosHDPhi2016__1up','MJClosHDPhi2017__1up','MJClosHDPhi2018__1up',
                                     'MJClosLDPhi2016__1up','MJClosLDPhi2017__1up','MJClosLDPhi2018__1up',#MJ
                                    'vvUnc__1up',
                                    'vvUnc__1down'
                                    # gamma jet
                                    'GJetTrig__1up','GJetTrig__1down',
                                    'GJetCore__1up','GJetCore__1down',
                                    # e fake ph systematic uncertainties
                                    'EFakePhEn__1down','EFakePhEn__1up',
                                    'EFakePhBkgSub__1down','EFakePhBkgSub__1up',
                                    'EFakePhStat__1down','EFakePhStat__1up',
                                    'EFakePhWindow__1down','EFakePhWindow__1up',
                                    # jet fake ph systematic unc
                                    'JetFakePhStat__1down','JetFakePhStat__1up',
                                    'JetFakePhClos__1down','JetFakePhClos__1up',
                                    'JetFakePhTightDef__1down','JetFakePhTightDef__1up',
                                        #'JET_QG_nchargedExp__1down','JET_QG_nchargedExp__1up','JET_QG_nchargedME__1down','JET_QG_nchargedME__1up','JET_QG_nchargedPDF__1down','JET_QG_nchargedPDF__1up','JET_QG_trackEfficiency','JET_QG_trackFakes','JET_QG_trackeff'
                                        ]
            # add the theory systematics
            self.systematicsList += self.systematicsVBFSignal+self.systematicsSignalPDF + self.systematicsGGFSignal

            # add the V+jets theory uncertainties
            self.systematicsList += self.systematicsZewkTheory
            self.systematicsList += self.systematicsWewkTheory
            self.systematicsList += self.systematicsZstrongTheory
            self.systematicsList += self.systematicsWstrongTheory

            # Filter out the unwanted systematics 
            systematicsList_tmp = []
            for s in self.systematicsList:
                filtFound=False
                for filt in self.removeList:
                    if s.find(filt)>-0.5:
                        print 'Systematic was filtered out: ',s
                        filtFound=True
                        break
                if len(self.allowList)>0:
                    skipAllow=True
                    for allow in self.allowList:
                        if s.find(allow)>-0.5:
                            skipAllow=False
                            break
                    if skipAllow:
                        continue
                if not filtFound:
                    systematicsList_tmp+=[s]
            self.systematicsList = systematicsList_tmp

        elif mode == "Nominal":
            self.systematicsList = ["Nominal"]
        elif mode == "WeightSyst":
            self.systematicsList = ['FT_EFF_B_systematics__1down','FT_EFF_B_systematics__1up','FT_EFF_C_systematics__1down','FT_EFF_C_systematics__1up','FT_EFF_Light_systematics__1down','FT_EFF_Light_systematics__1up','FT_EFF_extrapolation__1down','FT_EFF_extrapolation__1up','FT_EFF_extrapolation_from_charm__1down','FT_EFF_extrapolation_from_charm__1up','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down','eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up','JET_fJvtEfficiency__1down','JET_fJvtEfficiency__1up','JET_JvtEfficiency__1down','JET_JvtEfficiency__1up','MUON_EFF_TrigStatUncertainty__1down','MUON_EFF_TrigStatUncertainty__1up','MUON_EFF_TrigSystUncertainty__1down','MUON_EFF_TrigSystUncertainty__1up','MUON_EFF_BADMUON_SYS__1down','MUON_EFF_BADMUON_SYS__1up','MUON_EFF_ISO_STAT__1down','MUON_EFF_ISO_STAT__1up','MUON_EFF_ISO_SYS__1down','MUON_EFF_ISO_SYS__1up','MUON_EFF_RECO_STAT_LOWPT__1down','MUON_EFF_RECO_STAT_LOWPT__1up','MUON_EFF_RECO_STAT__1down','MUON_EFF_RECO_STAT__1up','MUON_EFF_RECO_SYS_LOWPT__1down','MUON_EFF_RECO_SYS_LOWPT__1up','MUON_EFF_RECO_SYS__1down','MUON_EFF_RECO_SYS__1up','MUON_EFF_TTVA_STAT__1down','MUON_EFF_TTVA_STAT__1up','MUON_EFF_TTVA_SYS__1down','MUON_EFF_TTVA_SYS__1up','PRW_DATASF__1down','PRW_DATASF__1up','xeSFTrigWeight__1up','xeSFTrigWeight__1down','puSyst2018Weight__1up','puSyst2018Weight__1down',
                                    'MJUnc__1up','MJClos2016__1up','MJClos2017__1up','MJClos2018__1up','MJClosHDPhi2016__1up','MJClosHDPhi2017__1up','MJClosHDPhi2018__1up',
                                     'MJClosLDPhi2016__1up','MJClosLDPhi2017__1up','MJClosLDPhi2018__1up','vvUnc__1up',
                                        'vvUnc__1down',
                                    'muoANTISFEL_EFF_ID__1down','muoANTISFEL_EFF_ID__1up']
            self.systematicsList = ['EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up',
'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','JET_JvtEfficiency__1down','JET_JvtEfficiency__1up','JET_fJvtEfficiency__1down','JET_fJvtEfficiency__1up','MUON_EFF_BADMUON_SYS__1down','MUON_EFF_BADMUON_SYS__1up','MUON_EFF_ISO_STAT__1down','MUON_EFF_ISO_STAT__1up','MUON_EFF_ISO_SYS__1down','MUON_EFF_ISO_SYS__1up','MUON_EFF_RECO_STAT__1down','MUON_EFF_RECO_STAT__1up','MUON_EFF_RECO_STAT_LOWPT__1down','MUON_EFF_RECO_STAT_LOWPT__1up','MUON_EFF_RECO_SYS__1down','MUON_EFF_RECO_SYS__1up','MUON_EFF_RECO_SYS_LOWPT__1down','MUON_EFF_RECO_SYS_LOWPT__1up','MUON_EFF_TTVA_STAT__1down','MUON_EFF_TTVA_STAT__1up','MUON_EFF_TTVA_SYS__1down','MUON_EFF_TTVA_SYS__1up','MUON_EFF_TrigStatUncertainty__1down','MUON_EFF_TrigStatUncertainty__1up','MUON_EFF_TrigSystUncertainty__1down','MUON_EFF_TrigSystUncertainty__1up',
'PH_EFF_ID_Uncertainty__1down','PH_EFF_ID_Uncertainty__1up','PH_EFF_ISO_Uncertainty__1down','PH_EFF_ISO_Uncertainty__1up','PH_EFF_TRIGGER_Uncertainty__1down','PH_EFF_TRIGGER_Uncertainty__1up',
                                    'PRW_DATASF__1down','PRW_DATASF__1up','xeSFTrigWeight__1up','xeSFTrigWeight__1down','JET_QG_nchargedExp__1down','JET_QG_nchargedExp__1up','JET_QG_nchargedME__1down','JET_QG_nchargedME__1up','JET_QG_nchargedPDF__1down','JET_QG_nchargedPDF__1up','JET_QG_trackEfficiency','JET_QG_trackFakes','JET_QG_trackeff',
                                    'puSyst2018Weight__1up','puSyst2018Weight__1down',
                                    #'MJUnc__1up','MJClos2016__1up','MJClos2017__1up','MJClos2018__1up','MJClosHDPhi2016__1up','MJClosHDPhi2017__1up','MJClosHDPhi2018__1up',
                                     #'MJClosLDPhi2016__1up','MJClosLDPhi2017__1up','MJClosLDPhi2018__1up','vvUnc__1up',
                                        'vvUnc__1down',
                                    'muoANTISFEL_EFF_ID__1down','muoANTISFEL_EFF_ID__1up',
                                        ]
            self.systematicsList += ['ATLAS_PDF4LHC_NLO_30_EV30__1up','ATLAS_PDF4LHC_NLO_30_EV29__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV28__1up','ATLAS_PDF4LHC_NLO_30_EV27__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV26__1up','ATLAS_PDF4LHC_NLO_30_EV25__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV24__1up','ATLAS_PDF4LHC_NLO_30_EV23__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV22__1up','ATLAS_PDF4LHC_NLO_30_EV21__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV20__1up','ATLAS_PDF4LHC_NLO_30_EV19__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV18__1up','ATLAS_PDF4LHC_NLO_30_EV17__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV16__1up','ATLAS_PDF4LHC_NLO_30_EV15__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV14__1up','ATLAS_PDF4LHC_NLO_30_EV13__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV12__1up','ATLAS_PDF4LHC_NLO_30_EV11__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV10__1up','ATLAS_PDF4LHC_NLO_30_EV9__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV8__1up','ATLAS_PDF4LHC_NLO_30_EV7__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV6__1up','ATLAS_PDF4LHC_NLO_30_EV5__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV4__1up','ATLAS_PDF4LHC_NLO_30_EV3__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV2__1up','ATLAS_PDF4LHC_NLO_30_EV1__1up',
                                    'VBF_qqH_25__1up','VBF_qqH_2jet__1up',
                                    'VBF_qqH_Mjj1500__1up','VBF_qqH_Mjj1000__1up',
                                    'VBF_qqH_Mjj700__1up','VBF_qqH_Mjj350__1up',
                                    'VBF_qqH_Mjj120__1up','VBF_qqH_Mjj60__1up',
                                     'VBF_qqH_200__1up','VBF_qqH_tot__1up',
                                     "ggF_gg2H_mu__1down","ggF_gg2H_res__1down","ggF_gg2H_qm_t__1down",
                                         "ggF_gg2H_mig01__1down","ggF_gg2H_mig12__1down","ggF_gg2H_vbf2j__1down",
                                         "ggF_gg2H_vbf3j__1down","ggF_gg2H_pTH60__1down","ggF_gg2H_pTH120__1down"
                                     'nloEWKWeight__1up','nloEWKWeight__1down',
                                     'VBF_qqgamH_PSVar__1down','VBF_qqgamH_PSVar__1up',
                                     'VBF_qqgamH_Scale__1down','VBF_qqgamH_Scale__1up',
                                     #MJ
                                     'MJUnc__1up','MJClos2016__1up','MJClos2017__1up','MJClos2018__1up','MJClosHDPhi2016__1up','MJClosHDPhi2017__1up','MJClosHDPhi2018__1up',
                                     'MJClosLDPhi2016__1up','MJClosLDPhi2017__1up',
                                      'PH_EFF_ID_Uncertainty__1down','PH_EFF_ID_Uncertainty__1up',
                                     'PH_EFF_ISO_Uncertainty__1down','PH_EFF_ISO_Uncertainty__1up',
                                     # gamma jet
                                    'GJetTrig__1up','GJetTrig__1down',
                                    'GJetCore__1up','GJetCore__1down',
                                    # e fake ph systematic uncertainties
                                    'EFakePhEn__1down','EFakePhEn__1up',
                                    'EFakePhBkgSub__1down','EFakePhBkgSub__1up',
                                    'EFakePhStat__1down','EFakePhStat__1up',
                                    'EFakePhWindow__1down','EFakePhWindow__1up',
                                    # jet fake ph systematic unc
                                    'JetFakePhStat__1down','JetFakePhStat__1up',
                                    'JetFakePhClos__1down','JetFakePhClos__1up',
                                    'JetFakePhTightDef__1down','JetFakePhTightDef__1up',]            
            self.systematicsList+=self.systematicsVBFSignal+self.systematicsSignalPDF + self.systematicsGGFSignal
            # add the V+jets theory uncertainties
            self.systematicsList += self.systematicsZewkTheory
            self.systematicsList += self.systematicsWewkTheory
            self.systematicsList += self.systematicsZstrongTheory
            self.systematicsList += self.systematicsWstrongTheory

        elif mode == "gjet":
            # gamma jet
            self.systematicsList = ['Nominal','GJetTrig__1up','GJetTrig__1down',
                                    'GJetCore__1up','GJetCore__1down',]
        elif mode == "efakeph":
                                    # e fake ph systematic uncertainties
            self.systematicsList = ['Nominal','EFakePhEn__1down','EFakePhEn__1up',
                                    'EFakePhBkgSub__1down','EFakePhBkgSub__1up',
                                    'EFakePhStat__1down','EFakePhStat__1up',
                                    'EFakePhWindow__1down','EFakePhWindow__1up']
        elif mode == "jfakeph":
                                    # jet fake ph systematic unc
            self.systematicsList = ['Nominal','JetFakePhStat__1down','JetFakePhStat__1up',
                                    'JetFakePhClos__1down','JetFakePhClos__1up',
                                    'JetFakePhTightDef__1down','JetFakePhTightDef__1up']
        elif mode == "Electrons":
            self.systematicsList = ["Nominal", "EG_RESOLUTION_ALL__1down", "EG_RESOLUTION_ALL__1up", "EG_SCALE_ALL__1down", "EG_SCALE_ALL__1up", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down",  "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up"]
        elif mode == "Muons":
            self.systematicsList = ["MUON_EFF_STAT__1down", "MUON_EFF_STAT__1up", "MUON_EFF_SYS__1down", "MUON_EFF_SYS__1up", "MUON_EFF_TrigStatUncertainty__1down", "MUON_EFF_TrigStatUncertainty__1up", "MUON_EFF_TrigSystUncertainty__1down", "MUON_EFF_TrigSystUncertainty__1up", "MUON_ID__1down", "MUON_ID__1up", "MUON_ISO_STAT__1down", "MUON_ISO_STAT__1up", "MUON_ISO_SYS__1down", "MUON_ISO_SYS__1up", "MUON_MS__1down", "MUON_MS__1up", "MUON_SAGITTA_RESBIAS__1down", "MUON_SAGITTA_RESBIAS__1up", "MUON_SAGITTA_RHO__1down", "MUON_SAGITTA_RHO__1up", "MUON_SCALE__1down", "MUON_SCALE__1up", "MUON_TTVA_STAT__1down", "MUON_TTVA_STAT__1up", "MUON_TTVA_SYS__1down", "MUON_TTVA_SYS__1up"]
        elif mode == "QG":
            self.systematicsList = ['JET_QG_nchargedExp__1down','JET_QG_nchargedExp__1up','JET_QG_nchargedME__1down','JET_QG_nchargedME__1up','JET_QG_nchargedPDF__1down','JET_QG_nchargedPDF__1up','JET_QG_trackEfficiency','JET_QG_trackFakes','JET_QG_trackeff']#,' JET_QG_fake'            
        elif mode == "JES":            
            self.systematicsList = ['Nominal','JET_BJES_Response__1down','JET_BJES_Response__1up',
                                       'JET_EffectiveNP_Detector1__1down','JET_EffectiveNP_Detector1__1up','JET_EffectiveNP_Detector2__1down','JET_EffectiveNP_Detector2__1up',
                                       'JET_EffectiveNP_Mixed1__1down','JET_EffectiveNP_Mixed1__1up','JET_EffectiveNP_Mixed2__1down','JET_EffectiveNP_Mixed2__1up','JET_EffectiveNP_Mixed3__1down','JET_EffectiveNP_Mixed3__1up',
                                       'JET_EffectiveNP_Modelling1__1down','JET_EffectiveNP_Modelling1__1up','JET_EffectiveNP_Modelling2__1down','JET_EffectiveNP_Modelling2__1up','JET_EffectiveNP_Modelling3__1down','JET_EffectiveNP_Modelling3__1up','JET_EffectiveNP_Modelling4__1down','JET_EffectiveNP_Modelling4__1up',
                                       'JET_EffectiveNP_Statistical1__1down','JET_EffectiveNP_Statistical1__1up','JET_EffectiveNP_Statistical2__1down','JET_EffectiveNP_Statistical2__1up','JET_EffectiveNP_Statistical3__1down','JET_EffectiveNP_Statistical3__1up','JET_EffectiveNP_Statistical4__1down','JET_EffectiveNP_Statistical4__1up','JET_EffectiveNP_Statistical5__1down','JET_EffectiveNP_Statistical5__1up','JET_EffectiveNP_Statistical6__1down','JET_EffectiveNP_Statistical6__1up',
                                       'JET_EtaIntercalibration_Modelling__1down','JET_EtaIntercalibration_Modelling__1up','JET_EtaIntercalibration_NonClosure_highE__1down','JET_EtaIntercalibration_NonClosure_highE__1up','JET_EtaIntercalibration_NonClosure_negEta__1down','JET_EtaIntercalibration_NonClosure_negEta__1up','JET_EtaIntercalibration_NonClosure_posEta__1down','JET_EtaIntercalibration_NonClosure_posEta__1up','JET_EtaIntercalibration_TotalStat__1down','JET_EtaIntercalibration_TotalStat__1up',
                                       'JET_Flavor_Composition__1down','JET_Flavor_Composition__1up','JET_Flavor_Response__1down','JET_Flavor_Response__1up',
                                       'JET_JER_DataVsMC_MC16__1down','JET_JER_DataVsMC_MC16__1up',
                                    'JET_JER_EffectiveNP_1__1up',
                                    'JET_JER_EffectiveNP_2__1up',
                                    'JET_JER_EffectiveNP_3__1up',
                                    'JET_JER_EffectiveNP_4__1up',
                                    'JET_JER_EffectiveNP_5__1up',
                                    'JET_JER_EffectiveNP_6__1up',
                                    'JET_JER_EffectiveNP_7__1up',
                                        'JET_JER_EffectiveNP_8__1up','JET_JER_EffectiveNP_8__1down',
                                        'JET_JER_EffectiveNP_9__1up','JET_JER_EffectiveNP_9__1down',
                                        'JET_JER_EffectiveNP_10__1up','JET_JER_EffectiveNP_10__1down',
                                        'JET_JER_EffectiveNP_11__1up','JET_JER_EffectiveNP_11__1down',
                                        'JET_JER_EffectiveNP_12restTerm__1up','JET_JER_EffectiveNP_12restTerm__1down',
                                        #'JET_JER_EffectiveNP_7restTerm__1up',
                                       'JET_Pileup_OffsetMu__1down','JET_Pileup_OffsetMu__1up','JET_Pileup_OffsetNPV__1down','JET_Pileup_OffsetNPV__1up','JET_Pileup_PtTerm__1down','JET_Pileup_PtTerm__1up','JET_Pileup_RhoTopology__1down','JET_Pileup_RhoTopology__1up','JET_PunchThrough_MC16__1down','JET_PunchThrough_MC16__1up','JET_SingleParticle_HighPt__1down','JET_SingleParticle_HighPt__1up',
                                       'JET_fJvtEfficiency__1down','JET_fJvtEfficiency__1up','JET_JvtEfficiency__1down','JET_JvtEfficiency__1up', 
            ]
        elif mode == "MJsyst":
            self.systematicsList = ['EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up',
'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','JET_JvtEfficiency__1down','JET_JvtEfficiency__1up','JET_fJvtEfficiency__1down','JET_fJvtEfficiency__1up','MUON_EFF_BADMUON_SYS__1down','MUON_EFF_BADMUON_SYS__1up','MUON_EFF_ISO_STAT__1down','MUON_EFF_ISO_STAT__1up','MUON_EFF_ISO_SYS__1down','MUON_EFF_ISO_SYS__1up','MUON_EFF_RECO_STAT__1down','MUON_EFF_RECO_STAT__1up','MUON_EFF_RECO_STAT_LOWPT__1down','MUON_EFF_RECO_STAT_LOWPT__1up','MUON_EFF_RECO_SYS__1down','MUON_EFF_RECO_SYS__1up','MUON_EFF_RECO_SYS_LOWPT__1down','MUON_EFF_RECO_SYS_LOWPT__1up','MUON_EFF_TTVA_STAT__1down','MUON_EFF_TTVA_STAT__1up','MUON_EFF_TTVA_SYS__1down','MUON_EFF_TTVA_SYS__1up','MUON_EFF_TrigStatUncertainty__1down','MUON_EFF_TrigStatUncertainty__1up','MUON_EFF_TrigSystUncertainty__1down','MUON_EFF_TrigSystUncertainty__1up',
                                    'PRW_DATASF__1down','PRW_DATASF__1up','xeSFTrigWeight__1up','xeSFTrigWeight__1down',
                                    'puSyst2018Weight__1up','puSyst2018Weight__1down',
                                    'MJUnc__1up','MJClos2016__1up','MJClos2017__1up','MJClos2018__1up','MJClosHDPhi2016__1up','MJClosHDPhi2017__1up','MJClosHDPhi2018__1up',
                                     'MJClosLDPhi2016__1up','MJClosLDPhi2017__1up','MJClosLDPhi2018__1up','vvUnc__1up',
                                        'vvUnc__1down',
                                        'ATLAS_PDF4LHC_NLO_30_EV30__1up','ATLAS_PDF4LHC_NLO_30_EV29__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV28__1up','ATLAS_PDF4LHC_NLO_30_EV27__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV26__1up','ATLAS_PDF4LHC_NLO_30_EV25__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV24__1up','ATLAS_PDF4LHC_NLO_30_EV23__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV22__1up','ATLAS_PDF4LHC_NLO_30_EV21__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV20__1up','ATLAS_PDF4LHC_NLO_30_EV19__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV18__1up','ATLAS_PDF4LHC_NLO_30_EV17__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV16__1up','ATLAS_PDF4LHC_NLO_30_EV15__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV14__1up','ATLAS_PDF4LHC_NLO_30_EV13__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV12__1up','ATLAS_PDF4LHC_NLO_30_EV11__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV10__1up','ATLAS_PDF4LHC_NLO_30_EV9__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV8__1up','ATLAS_PDF4LHC_NLO_30_EV7__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV6__1up','ATLAS_PDF4LHC_NLO_30_EV5__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV4__1up','ATLAS_PDF4LHC_NLO_30_EV3__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV2__1up','ATLAS_PDF4LHC_NLO_30_EV1__1up',
                                    'VBF_qqH_25__1up','VBF_qqH_2jet__1up',
                                    'VBF_qqH_Mjj1500__1up','VBF_qqH_Mjj1000__1up',
                                    'VBF_qqH_Mjj700__1up','VBF_qqH_Mjj350__1up',
                                    'VBF_qqH_Mjj120__1up','VBF_qqH_Mjj60__1up',
                                     'VBF_qqH_200__1up','VBF_qqH_tot__1up',
                                        "ggF_gg2H_mu__1down","ggF_gg2H_res__1down","ggF_gg2H_qm_t__1down",
                                         "ggF_gg2H_mig01__1down","ggF_gg2H_mig12__1down","ggF_gg2H_vbf2j__1down",
                                         "ggF_gg2H_vbf3j__1down","ggF_gg2H_pTH60__1down","ggF_gg2H_pTH120__1down"]
        elif mode == "ANTISF":            
            self.systematicsList = ['Nominal','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','muoANTISFEL_EFF_ID__1down','muoANTISFEL_EFF_ID__1up']
        elif mode == "gam":
            self.systematicsList = ['Nominal','GJetTrig__1up','GJetTrig__1down','GJetCore__1up','GJetCore__1down','EFakePhEn__1down','EFakePhEn__1up','EFakePhBkgSub__1down','EFakePhBkgSub__1up','EFakePhStat__1down','EFakePhStat__1up','EFakePhWindow__1down','EFakePhWindow__1up','JetFakePhStat__1down','JetFakePhStat__1up','PRW_DATASF__1down','PRW_DATASF__1up','JET_JER_DataVsMC_MC16__1up']#,'JET_JER_DataVsMC_MC16__1down','JET_JER_DataVsMC_MC16__1up']#'xeSFTrigWeight__1up','xeSFTrigWeight__1down',
        elif mode == "JER":
            self.systematicsList = ['Nominal', 'JET_JER_DataVsMC_MC16__1up', 'JET_JER_DataVsMC_MC16__1down', 'JET_JER_DataVsMC__1up', 'JET_JER_EffectiveNP_1__1up', 'JET_JER_EffectiveNP_2__1up', 'JET_JER_EffectiveNP_3__1up', 'JET_JER_EffectiveNP_4__1up', 'JET_JER_EffectiveNP_5__1up', 'JET_JER_EffectiveNP_6__1up',
                                        'JET_JER_EffectiveNP_7__1up',
                                        'JET_JER_EffectiveNP_8__1up','JET_JER_EffectiveNP_8__1down',
                                        'JET_JER_EffectiveNP_9__1up','JET_JER_EffectiveNP_9__1down',
                                        'JET_JER_EffectiveNP_10__1up','JET_JER_EffectiveNP_10__1down',
                                        'JET_JER_EffectiveNP_11__1up','JET_JER_EffectiveNP_11__1down',
                                        'JET_JER_EffectiveNP_12restTerm__1up','JET_JER_EffectiveNP_12restTerm__1down',
                                        #'JET_JER_EffectiveNP_7restTerm__1up',
                                        ]
        elif mode == "Pileup":
            self.systematicsList = ['Nominal','JET_Pileup_OffsetMu__1down','JET_Pileup_OffsetMu__1up',
                                    'JET_Pileup_OffsetNPV__1down','JET_Pileup_OffsetNPV__1up',
                                    'JET_Pileup_PtTerm__1down','JET_Pileup_PtTerm__1up',
                                    'JET_Pileup_RhoTopology__1down','JET_Pileup_RhoTopology__1up',]
        elif mode == "xeSFTrig":
            self.systematicsList = ['Nominal','xeSFTrigWeight__1up','xeSFTrigWeight__1down']

        elif mode == "METSystOpt":
            self.systematicsList = ['Nominal', 'xeSFTrigWeight__1up','xeSFTrigWeight__1down','JET_JvtEfficiency__1down','JET_JvtEfficiency__1up',
                                    'JET_fJvtEfficiency__1down','JET_fJvtEfficiency__1up',
                                    'JET_EffectiveNP_Mixed1__1down','JET_EffectiveNP_Mixed1__1up',
                                    'JET_EtaIntercalibration_Modelling__1up','JET_EtaIntercalibration_Modelling__1down',
                                    'JET_EffectiveNP_Modelling1__1up','JET_EffectiveNP_Modelling1__1down',
                                    'JET_JER_EffectiveNP_1__1up',
                                    'JET_JER_DataVsMC_MC16__1up', 'JET_JER_DataVsMC_MC16__1down',
                                    'JET_Pileup_OffsetMu__1down','JET_Pileup_OffsetMu__1up',
                                    'JET_Pileup_OffsetNPV__1down','JET_Pileup_OffsetNPV__1up',
                                    'JET_Pileup_PtTerm__1down','JET_Pileup_PtTerm__1up',
                                    'JET_Pileup_RhoTopology__1down','JET_Pileup_RhoTopology__1up',
                                ]
        elif mode == "SigTheory":
            self.systematicsList=self.systematicsVBFSignal+self.systematicsSignalPDF + self.systematicsGGFSignal
        elif mode == "VjetTheory":
            # add the V+jets theory uncertainties
            self.systematicsList = self.systematicsZewkTheory
            self.systematicsList += self.systematicsWewkTheory
            self.systematicsList += self.systematicsZstrongTheory
            self.systematicsList += self.systematicsWstrongTheory

        elif mode == "OneSided": # this is used to list all systematics that need to by symmeterized in plotting
            self.systematicsList = ["MET_SoftTrk_ResoPara", "MET_SoftTrk_ResoPerp",#'JET_JER_DataVsMC_MC16__1up',
                                        'JET_JER_DataVsMC__1up', 'JET_JER_EffectiveNP_1__1up', 'JET_JER_EffectiveNP_2__1up', 'JET_JER_EffectiveNP_3__1up',
                                        'JET_JER_EffectiveNP_4__1up', 'JET_JER_EffectiveNP_5__1up', 'JET_JER_EffectiveNP_6__1up',
                                        #'JET_JER_EffectiveNP_7restTerm__1up','JET_JER_DataVsMC_MC16__1up',
                                        'JET_QG_trackFakes','JET_QG_trackeff']
            # add theory systematics
            self.systematicsList += ['ATLAS_PDF4LHC_NLO_30_EV30__1up','ATLAS_PDF4LHC_NLO_30_EV29__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV28__1up','ATLAS_PDF4LHC_NLO_30_EV27__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV26__1up','ATLAS_PDF4LHC_NLO_30_EV25__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV24__1up','ATLAS_PDF4LHC_NLO_30_EV23__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV22__1up','ATLAS_PDF4LHC_NLO_30_EV21__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV20__1up','ATLAS_PDF4LHC_NLO_30_EV19__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV18__1up','ATLAS_PDF4LHC_NLO_30_EV17__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV16__1up','ATLAS_PDF4LHC_NLO_30_EV15__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV14__1up','ATLAS_PDF4LHC_NLO_30_EV13__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV12__1up','ATLAS_PDF4LHC_NLO_30_EV11__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV10__1up','ATLAS_PDF4LHC_NLO_30_EV9__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV8__1up','ATLAS_PDF4LHC_NLO_30_EV7__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV6__1up','ATLAS_PDF4LHC_NLO_30_EV5__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV4__1up','ATLAS_PDF4LHC_NLO_30_EV3__1up',
                                     'ATLAS_PDF4LHC_NLO_30_EV2__1up','ATLAS_PDF4LHC_NLO_30_EV1__1up',
                                    'VBF_qqH_25__1up','VBF_qqH_2jet__1up',
                                    'VBF_qqH_Mjj1500__1up','VBF_qqH_Mjj1000__1up',
                                    'VBF_qqH_Mjj700__1up','VBF_qqH_Mjj350__1up',
                                    'VBF_qqH_Mjj120__1up','VBF_qqH_Mjj60__1up',
                                     'VBF_qqH_200__1up','VBF_qqH_tot__1up',
                                     "ggF_gg2H_mu__1down","ggF_gg2H_res__1down","ggF_gg2H_qm_t__1down",
                                         "ggF_gg2H_mig01__1down","ggF_gg2H_mig12__1down","ggF_gg2H_vbf2j__1down",
                                         "ggF_gg2H_vbf3j__1down","ggF_gg2H_pTH60__1down","ggF_gg2H_pTH120__1down"
                                     #'JetFakePhTight5__1up','JetFakePhTight3__1up',
                                     #MJ
                                     'MJUnc__1up','MJClos2016__1up','MJClos2017__1up','MJClos2018__1up','MJClosHDPhi2016__1up','MJClosHDPhi2017__1up','MJClosHDPhi2018__1up',
                                     'MJClosLDPhi2016__1up','MJClosLDPhi2017__1up','MJClosLDPhi2018__1up']
        elif mode == "OneSidedDown": # this is used to list all systematics that need to by symmeterized in plotting
            self.systematicsList = self.systematicsListDown
            
    def getsystematicsList(self):
        tmp_systematicsList = self.Filter(self.systematicsList);
        return tmp_systematicsList
    
    def getsystematicsListWithDown(self):
        tmp_systematicsList = self.Filter(self.systematicsList);        
        downList = self.Filter(self.systematicsListDown);
        return tmp_systematicsList+downList

    def getsystematicsOneSidedMap(self):
        inmap= {#'JET_JER_DataVsMC__1down':'JET_JER_DataVsMC__1up', # these are old!
                #'JET_JER_DataVsMC_MC16__1down':'JET_JER_DataVsMC_MC16__1up', # this is two sided
                'JET_JER_EffectiveNP_1__1down':'JET_JER_EffectiveNP_1__1up',
                'JET_JER_EffectiveNP_2__1down':'JET_JER_EffectiveNP_2__1up',
                'JET_JER_EffectiveNP_3__1down':'JET_JER_EffectiveNP_3__1up',
                'JET_JER_EffectiveNP_4__1down':'JET_JER_EffectiveNP_4__1up',
                'JET_JER_EffectiveNP_5__1down':'JET_JER_EffectiveNP_5__1up',
                'JET_JER_EffectiveNP_6__1down':'JET_JER_EffectiveNP_6__1up',
                'JET_JER_EffectiveNP_7__1down':'JET_JER_EffectiveNP_7__1up',
                #'JET_JER_EffectiveNP_7restTerm__1down':'JET_JER_EffectiveNP_7restTerm__1up',
                'ATLAS_PDF4LHC_NLO_30_EV30__1down':'ATLAS_PDF4LHC_NLO_30_EV30__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV29__1down':'ATLAS_PDF4LHC_NLO_30_EV29__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV28__1down':'ATLAS_PDF4LHC_NLO_30_EV28__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV27__1down':'ATLAS_PDF4LHC_NLO_30_EV27__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV26__1down':'ATLAS_PDF4LHC_NLO_30_EV26__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV25__1down':'ATLAS_PDF4LHC_NLO_30_EV25__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV24__1down':'ATLAS_PDF4LHC_NLO_30_EV24__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV23__1down':'ATLAS_PDF4LHC_NLO_30_EV23__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV22__1down':'ATLAS_PDF4LHC_NLO_30_EV22__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV21__1down':'ATLAS_PDF4LHC_NLO_30_EV21__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV20__1down':'ATLAS_PDF4LHC_NLO_30_EV20__1up',
                'ATLAS_PDF4LHC_NLO_30_EV19__1down':'ATLAS_PDF4LHC_NLO_30_EV19__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV18__1down':'ATLAS_PDF4LHC_NLO_30_EV18__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV17__1down':'ATLAS_PDF4LHC_NLO_30_EV17__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV16__1down':'ATLAS_PDF4LHC_NLO_30_EV16__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV15__1down':'ATLAS_PDF4LHC_NLO_30_EV15__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV14__1down':'ATLAS_PDF4LHC_NLO_30_EV14__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV13__1down':'ATLAS_PDF4LHC_NLO_30_EV13__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV12__1down':'ATLAS_PDF4LHC_NLO_30_EV12__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV11__1down':'ATLAS_PDF4LHC_NLO_30_EV11__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV10__1down':'ATLAS_PDF4LHC_NLO_30_EV10__1up',
                'ATLAS_PDF4LHC_NLO_30_EV9__1down':'ATLAS_PDF4LHC_NLO_30_EV9__1up',
                'ATLAS_PDF4LHC_NLO_30_EV8__1down':'ATLAS_PDF4LHC_NLO_30_EV8__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV7__1down':'ATLAS_PDF4LHC_NLO_30_EV7__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV6__1down':'ATLAS_PDF4LHC_NLO_30_EV6__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV5__1down':'ATLAS_PDF4LHC_NLO_30_EV5__1up',
                'ATLAS_PDF4LHC_NLO_30_EV4__1down':'ATLAS_PDF4LHC_NLO_30_EV4__1up',               
                'ATLAS_PDF4LHC_NLO_30_EV3__1down':'ATLAS_PDF4LHC_NLO_30_EV3__1up',                
                'ATLAS_PDF4LHC_NLO_30_EV2__1down':'ATLAS_PDF4LHC_NLO_30_EV2__1up',
                'ATLAS_PDF4LHC_NLO_30_EV1__1down':'ATLAS_PDF4LHC_NLO_30_EV1__1up',
                "ggF_gg2H_mu__1down":"ggF_gg2H_mu__1up",
                "ggF_gg2H_res__1down":"ggF_gg2H_res__1up",
                "ggF_gg2H_qm_t__1down":"ggF_gg2H_qm_t__1up",
                "ggF_gg2H_mig01__1down":"ggF_gg2H_mig01__1up",
                "ggF_gg2H_mig12__1down":"ggF_gg2H_mig12__1up",
                "ggF_gg2H_vbf2j__1down":"ggF_gg2H_vbf2j__1up",
                "ggF_gg2H_vbf3j__1down":"ggF_gg2H_vbf3j__1up",
                "ggF_gg2H_pTH60__1down":"ggF_gg2H_pTH60__1up",
                "ggF_gg2H_pTH120__1down":"ggF_gg2H_pTH120__1up",
                
                "JET_JER_SINGLE_NP__1down":"JET_JER_SINGLE_NP__1up",
                #"JET_QG_trackFakes__1down":"JET_QG_trackFakes",
                #"JET_QG_trackeff__1down"  :"JET_QG_trackeff",
                #"JetFakePhTight5__1down"  :"JetFakePhTight5__1up",
                #"JetFakePhTight3__1down"  :"JetFakePhTight3__1up",
                "MET_SoftTrk_ResoParaDown":"MET_SoftTrk_ResoPara",
                "MET_SoftTrk_ResoPerpDown":"MET_SoftTrk_ResoPerp",}
        if not self.photon_ana:
            inmap['MJUnc__1down' ]= 'MJUnc__1up'
            inmap['MJClos2016__1down' ]= 'MJClos2016__1up'
            inmap['MJClos2017__1down' ]= 'MJClos2017__1up'
            inmap['MJClos2018__1down' ]= 'MJClos2018__1up'
            inmap['MJClosHDPhi2016__1down' ]= 'MJClosHDPhi2016__1up'
            inmap['MJClosHDPhi2017__1down' ]= 'MJClosHDPhi2017__1up'
            inmap['MJClosHDPhi2018__1down' ]= 'MJClosHDPhi2018__1up'
            inmap['MJClosLDPhi2016__1down' ]= 'MJClosLDPhi2016__1up'
            inmap['MJClosLDPhi2017__1down' ]= 'MJClosLDPhi2017__1up'
            inmap['MJClosLDPhi2018__1down' ]= 'MJClosLDPhi2018__1up'
            inmap['VBF_qqH_25__1down']='VBF_qqH_25__1up'
            inmap['VBF_qqH_2jet__1down']='VBF_qqH_2jet__1up'
            inmap['VBF_qqH_Mjj1500__1down']='VBF_qqH_Mjj1500__1up'
            inmap['VBF_qqH_Mjj1000__1down']='VBF_qqH_Mjj1000__1up'
            inmap['VBF_qqH_Mjj700__1down']='VBF_qqH_Mjj700__1up'
            inmap['VBF_qqH_Mjj350__1down']='VBF_qqH_Mjj350__1up'
            inmap['VBF_qqH_Mjj120__1down']='VBF_qqH_Mjj120__1up'
            inmap['VBF_qqH_Mjj60__1down']='VBF_qqH_Mjj60__1up'
            inmap['VBF_qqH_200__1down']='VBF_qqH_200__1up'
            inmap['VBF_qqH_tot__1down']='VBF_qqH_tot__1up'
        return inmap

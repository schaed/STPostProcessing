#include "VJetsMjjSystHelper.h"

#include <TF1.h>
#include <TH1.h>
#include <TFile.h>
#include <TGraphAsymmErrors.h>
#include <TObjArray.h>
#include <TCanvas.h>
#include <iostream>

VJetsMjjSystHelper::VJetsMjjSystHelper()
{
   m_initialized = false;
   m_inputName = "input/theoretical_wToz_mjj_corrections.root";
   m_histoQCDMap.clear();
   m_histoEWKMap.clear();   
   m_variations.clear();
   m_applyEWCorrection["vvj"] = true;
   m_applyQCDCorrection["vvj"] = true;
   m_applyEWCorrection["evj"] = true;
   m_applyQCDCorrection["evj"] = true;
   //m_applyEWCorrection["vvj"] = true;
   //m_applyQCDCorrection["vvj"] = true;
   m_nominalOnly = false;
   m_debug = false;
}

VJetsMjjSystHelper::~VJetsMjjSystHelper()
{

   for (std::map<TString, TH1*>::iterator itr = m_histoQCDMap.begin(); itr != m_histoQCDMap.end(); itr++) {
      delete itr->second;
      itr->second = 0;
   }
   for (std::map<TString, TH1*>::iterator itr = m_histoEWKMap.begin(); itr != m_histoEWKMap.end(); itr++) {
      delete itr->second;
      itr->second = 0;
   }   
   m_histoQCDMap.clear();
   m_histoEWKMap.clear();
   m_variations.clear();
}


void VJetsMjjSystHelper::setInputFileName(TString fname)
{
   m_inputName = fname;
}

void VJetsMjjSystHelper::applyEWCorrection(bool doApply, TString processes)
{

   TObjArray *tokens = processes.Tokenize(",");
   for (int iTok = 0; iTok < tokens->GetSize(); iTok++) {
      if (!tokens->At(iTok)) break;
      TString process = tokens->At(iTok)->GetName();
      m_applyEWCorrection[process] = doApply;
   }
}

void VJetsMjjSystHelper::applyQCDCorrection(bool doApply, TString processes)
{

   TObjArray *tokens = processes.Tokenize(",");
   for (int iTok = 0; iTok < tokens->GetSize(); iTok++) {
      if (!tokens->At(iTok)) break;
      TString process = tokens->At(iTok)->GetName();
      m_applyQCDCorrection[process] = doApply;
   }
}

int VJetsMjjSystHelper::initialize()
{

   std::vector<TString> variations = { "Nominal",
                                       "vjetsMjj_QCD_kQCD__1up", "vjetsMjj_QCD_kQCD__1down",
                                       "vjetsMjj_QCD_kPS__1up",  "vjetsMjj_QCD_kPS__1down",
                                       "vjetsMjj_QCD_kMix__1up", "vjetsMjj_QCD_kMix__1down",
                                       "vjetsMjj_QCD_kRew__1up", "vjetsMjj_QCD_kRew__1down",
				       // EWK uncertainties
				       "vjetsMjj_EWK_kQCD__1up", "vjetsMjj_EWK_kQCD__1down",
                                       "vjetsMjj_EWK_kPS__1up",  "vjetsMjj_EWK_kPS__1down",
                                       "vjetsMjj_EWK_kMix__1up", "vjetsMjj_EWK_kMix__1down",
                                       "vjetsMjj_EWK_kRew__1up", "vjetsMjj_EWK_kRew__1down",
                                     };
   if(m_nominalOnly){ variations.clear(); variations.push_back("Nominal"); }
   m_variations = variations;

   TFile *fIn = TFile::Open(m_inputName, "READ");

   std::vector<TString> processes = {"evj", "vvj"};

   for (unsigned int iP = 0; iP < processes.size(); iP++) {

      TString process = processes[iP];

      TString suffix = "";

      TH1 *hStrongRNLO         = getHisto(fIn, process + "_QCD_R_mjj_nominal");
      TH1 *hStrongdRNLOQCD     = getHisto(fIn, process + "_QCD_dR_mjj_QCD");
      TH1 *hStrongdRNLOPS      = getHisto(fIn, process + "_QCD_dR_mjj_PS");
      TH1 *hStrongdRNLOMix     = getHisto(fIn, process + "_QCD_dR_mjj_Mix");
      TH1 *hStrongdRNLORew     = getHisto(fIn, process + "_QCD_dR_mjj_Rew");

      TH1 *hEWKRNLO         = getHisto(fIn, process + "_EWK_R_mjj_nominal");
      TH1 *hEWKdRNLOQCD     = getHisto(fIn, process + "_EWK_dR_mjj_QCD");
      TH1 *hEWKdRNLOPS      = getHisto(fIn, process + "_EWK_dR_mjj_PS");
      TH1 *hEWKdRNLOMix     = getHisto(fIn, process + "_EWK_dR_mjj_Mix");
      TH1 *hEWKdRNLORew     = getHisto(fIn, process + "_EWK_dR_mjj_Rew");      

      for (unsigned int iVar = 0; iVar < m_variations.size(); iVar++) {

         TString variation = m_variations[iVar];
         TH1 *hMC_used = hStrongRNLO;

         TH1 *hVar = (TH1*)hMC_used->Clone(process + variation);
         hVar->SetDirectory(0);
         hVar->Reset();
	 TH1 *hVarEWKNom = nullptr;
	 if(variation=="Nominal"){
	   hVarEWKNom = (TH1*)hMC_used->Clone(process + variation+"_EWK");
	   hVarEWKNom->SetDirectory(0);
	   hVarEWKNom->Reset();
	 }
         for (int bin = 1; bin <= hMC_used->GetNbinsX() + 1; bin++) {

	   double sNNLO      = hStrongRNLO->GetBinContent(bin);
	   double kappa_QCD  = hStrongdRNLOQCD->GetBinContent(bin);
	   double kappa_PS   = hStrongdRNLOPS->GetBinContent(bin);
	   double kappa_Mix  = hStrongdRNLOMix->GetBinContent(bin);
	   double kappa_Rew  = hStrongdRNLORew->GetBinContent(bin);

	   if(variation.Contains("_EWK_k")){
	     sNNLO       = hEWKRNLO->GetBinContent(bin);
	     kappa_QCD   = hEWKdRNLOQCD->GetBinContent(bin);
	     kappa_PS    = hEWKdRNLOPS->GetBinContent(bin);
	     kappa_Mix   = hEWKdRNLOMix->GetBinContent(bin);
	     kappa_Rew   = hEWKdRNLORew->GetBinContent(bin);
	   }
	   
	   // set the sign
	   double sign=1.0;
	   if(variation.Contains("__1down")) sign=-1.0;
	   
	   // set the variation
	   if(variation.Contains("_kQCD")) sNNLO *= (1.0 + sign*kappa_QCD);
	   if(variation.Contains("_kPS") ) sNNLO *= (1.0 + sign*kappa_PS);
	   if(variation.Contains("_kMix")) sNNLO *= (1.0 + sign*kappa_Mix);
	   if(variation.Contains("_kRew")) sNNLO *= (1.0 + sign*kappa_Rew);
	   
	   hVar->SetBinContent(bin, sNNLO);

	   if(variation.Contains("Nominal")){
	     sNNLO       = hEWKRNLO->GetBinContent(bin);
	     hVarEWKNom->SetBinContent(bin, sNNLO);
	   }
	 }

	 if(variation.Contains("_EWK_k")){
	   m_histoEWKMap[hVar->GetName()] = hVar;
	 }else{
	   m_histoQCDMap[hVar->GetName()] = hVar;
	 }
	 // add the nominal EWK as only the QCD would be filled
	 if(variation.Contains("Nominal")){
	   m_histoEWKMap[hVar->GetName()] = hVarEWKNom;
	 }
      }
   }

   fIn->Clear();
   fIn->Close();
   delete fIn;
   m_initialized = true;
   std::cout << "INFO: VJetsMjjSystHelperInitialization completed" << std::endl;
   return 0;
}


const std::vector<TString> &VJetsMjjSystHelper::getAllVariationNames()
{

  static std::vector<TString> all_variation_names;

  for (auto variation: m_variations) {
    all_variation_names.push_back(variation);
  }

  if (!m_initialized) {
    std::cout << "ERROR: VJetsMjjSystHelper not initialized (called getAllVariationNames)" << std::endl;
    return all_variation_names;
  }

  return all_variation_names;

}

double VJetsMjjSystHelper::getCorrection(int mcChannelNumber, int n_lep, double mjj, TString variation)
{

   if (!m_initialized) {
      std::cout << "ERROR: VJetsMjjSystHelper not initialized" << std::endl;
      return 1;
   }

   bool isEWK=false;
   TString process = "";
   // Sherpa 2.2.1
   if ((364142 <= mcChannelNumber && mcChannelNumber <= 364155) || mcChannelNumber==364222 || mcChannelNumber==364223 ||
	    (366010 <= mcChannelNumber && mcChannelNumber <= 366017)  ||
	    (366019 <= mcChannelNumber && mcChannelNumber <= 366026)  ||
	    (366028 <= mcChannelNumber && mcChannelNumber <= 366035)) process = "vvj"; // Zvv
   else if ((364184 <= mcChannelNumber && mcChannelNumber <= 364197)||mcChannelNumber==364228||mcChannelNumber==364229) process = "evj"; // Wtv
   else if ((364156 <= mcChannelNumber && mcChannelNumber <= 364169)||mcChannelNumber==364224||mcChannelNumber==364225) process = "evj"; // Wuv
   else if ((364170 <= mcChannelNumber && mcChannelNumber <= 364183)||mcChannelNumber==364226||mcChannelNumber==364227) process = "evj"; // Wev
   else if ((364100 <= mcChannelNumber && mcChannelNumber <= 364113)||mcChannelNumber==364216||mcChannelNumber==364217) process = "vvj"; // Zuu
   else if ((364114 <= mcChannelNumber && mcChannelNumber <= 364127)||mcChannelNumber==364218||mcChannelNumber==364219) process = "vvj"; // Zee
   else if ((364128 <= mcChannelNumber && mcChannelNumber <= 364141)||mcChannelNumber==364220||mcChannelNumber==364221) process = "vvj"; // Ztt

   // add kT merged samples QCD 227 samples
   if(312496 <= mcChannelNumber && mcChannelNumber<=312531) process = "evj"; // Wlv
   else if(312448 <= mcChannelNumber && mcChannelNumber<=312483) process = "vvj"; // Zll
   else if(312484 <= mcChannelNumber && mcChannelNumber<=312495) process = "vvj"; // Znn

   // EWK samples powheg and sherpa
   if((308096 <= mcChannelNumber && mcChannelNumber<=308098) || (363237 <= mcChannelNumber && mcChannelNumber<=363239) || mcChannelNumber==830006 || mcChannelNumber==313395){
     process = "evj"; // Wlv
     isEWK=true;
   }else if((308092 <= mcChannelNumber && mcChannelNumber<=308094) || (363234 <= mcChannelNumber && mcChannelNumber<=363236) || mcChannelNumber==830007){
     process = "vvj"; // Zll
     isEWK=true;
   }else if(mcChannelNumber==363233 && mcChannelNumber==308095){
     process = "vvj"; // Znn
     isEWK=true;
   }

   if (process == "") return 1.;

   TH1 *hCorr;

   Double_t correction = 0;

   // load the nominal corrections
   std::map<TString, TH1*>::iterator itrQCD = m_histoQCDMap.find(process + "Nominal");
   std::map<TString, TH1*>::iterator itrEWK = m_histoEWKMap.find(process + "Nominal");
   if (itrQCD == m_histoQCDMap.end()) {
     std::cout << "Error: cannot find the QCD variation: " << std::endl;
     return 1;
   }
   if (itrEWK == m_histoEWKMap.end()) {
     std::cout << "Error: cannot find the EWK variation: " << std::endl;
     return 1;
   }

   // if this is a systematic variation, then check if the sample is EWK or QCD.
   // Check if the variation is EWK for EWK or QCD for QCD
   if(!variation.Contains("Nominal")){
     if(!isEWK && !variation.Contains("_EWK_k")){
       itrQCD = m_histoQCDMap.find(process + variation);
       if (itrQCD == m_histoQCDMap.end()) {
	 std::cout << "Error: unknown QCD variation: " << variation << std::endl;
	 return 1;
       }
     }else if(isEWK && variation.Contains("_EWK_k")){
       itrEWK = m_histoEWKMap.find(process + variation);
       if (itrEWK == m_histoEWKMap.end()) {
	 std::cout << "Error: unknown EWK variation: " << variation << std::endl;
	 return 1;
       }
     }
   }

   if(m_debug) std::cout << "isEWK: " << isEWK << " mjj: " << mjj << " variation: " << variation << std::endl;
   
   hCorr = itrQCD->second;
   if(isEWK) hCorr = itrEWK->second;
   if (mjj < hCorr->GetXaxis()->GetXmin()) return 1.0;
   if (mjj >= hCorr->GetXaxis()->GetXmax()) return 1.0;
   if(mjj<780.0) return 1.0;
   int bin = hCorr->FindBin(mjj);

   correction = hCorr->GetBinContent(bin);

   if(m_debug) std::cout << "    bin: " << bin << " correction: " << correction << std::endl;   
   // invert the correction for the lepton category
   if(n_lep>0){
     if(correction>0.0) correction=1.0/correction;
     else correction=1.0;
   }
   return correction;
}

TH1 *VJetsMjjSystHelper::getHisto(TDirectory *fIn, TString hname)
{

   TH1 *h = 0;

   if (!fIn || fIn->IsZombie()) {
      return h;
   }

   TObject *obj = fIn->Get(hname);
   if (!obj) {
      std::cout << "Error: object of name " << hname << " was not found in file " << fIn->GetName() << std::endl;
      return h;
   }

   h = (TH1*)obj->Clone();

   return h;
}

void VJetsMjjSystHelper::setNominalOnly(bool setNominalOnly){
  m_nominalOnly=setNominalOnly;
}

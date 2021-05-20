#ifndef VBFANALYSIS_VJETSMJJSYSTHELPER_H
#define VBFANALYSIS_VJETSMJJSYSTHELPER_H 1

#include <TString.h>
#include <map>
#include <vector>

class TH1;
class TF1;

class VJetsMjjSystHelper {

public:

  VJetsMjjSystHelper();
  ~VJetsMjjSystHelper();

  void setInputFileName(TString fname);
  void applyEWCorrection(bool doApply, TString processes = "evj,vvj");
  void applyQCDCorrection(bool doApply, TString processes = "evj,vvj");
  void setNominalOnly(bool setNominalOnly);
  TH1 *getHisto(TDirectory *fIn, TString hname);


  int initialize();

  const std::vector<TString> &getAllVariationNames();

  double getCorrection(int mcChannelNumber, int n_lep, double mjj, TString variation="Nominal");

private:

  bool m_initialized;
  TString m_inputName;
  std::map<TString, TH1*> m_histoQCDMap;
  std::map<TString, TH1*> m_histoEWKMap;  
  std::vector<TString> m_variations;
  std::map<TString, bool> m_applyEWCorrection;
  std::map<TString, bool> m_applyQCDCorrection;
  bool m_nominalOnly;
  bool m_debug;  
};

#endif

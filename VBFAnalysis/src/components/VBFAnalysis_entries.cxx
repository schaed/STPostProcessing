
#include "GaudiKernel/DeclareFactoryEntries.h"

#include "../VBFAnalysisAlg.h"
#include "../HFInputAlg.h"
#include "../VBFTruthAlg.h"
#include "../VBFVjetsAlg.h"
#include "../SignalSystHelper.h"
#include "../VJetsSystHelper.h"
#include "../VJetsMjjSystHelper.h"

DECLARE_ALGORITHM_FACTORY( VBFAnalysisAlg )
DECLARE_ALGORITHM_FACTORY( HFInputAlg )
DECLARE_ALGORITHM_FACTORY( VBFTruthAlg )
DECLARE_ALGORITHM_FACTORY( VBFVjetsAlg )
//DECLARE_ALGORITHM_FACTORY( SignalSystHelper )
//DECLARE_ALGORITHM_FACTORY( VJetsSystHelper )

DECLARE_FACTORY_ENTRIES( VBFAnalysis )
{
  DECLARE_ALGORITHM( VBFAnalysisAlg );
  DECLARE_ALGORITHM( HFInputAlg );
  DECLARE_ALGORITHM( VBFTruthAlg );
  DECLARE_ALGORITHM( VBFVjetsAlg );
  //DECLARE_ALGORITHM( SignalSystHelper );
  //DECLARE_ALGORITHM( VJetsSystHelper );
}

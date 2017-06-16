// -*-  C++  -*-

#ifndef RELAXATION_SWG
#define RELAXATION_SWG

//Copied following section from cfiddlenodes, but changed certain things

%module relaxation

%include "common/typemaps.swg"
%include "engine/typemaps.swg"
%extern "engine/cskeletonmodifier.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/relaxation.h" //Additional line added  
#include "engine/cskeletonmodifier.h"
#include "engine/cskeleton2.h"
%}

%pragma(python) include="engine/relaxation.spy"
   
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierPtr, CSkeletonModifierBasePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkelModCriterionPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeleton2 import CDeputySkeletonPtr"

//End introductory statements

class Relax : public CSkeletonModifier {
  public:
  Relax(double alpha, double gamma, int iterations);
  double getAlpha();
  double getGamma();
  double getIterations();
  void updateNodePositionsC(CDeputySkeleton* skeleton, FEMesh* mesh);
  
};


#endif //RELAXATION_SWG

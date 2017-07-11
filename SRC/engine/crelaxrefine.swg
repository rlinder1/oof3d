// -*- C++ -*-

#ifndef CRELAXREFINE_SWG
#define CRELAXREFINE_SWG

%module crelaxrefine

//Copied from csnaprefine.swg and relaxation.swg

%include "engine/typemaps.swg"
%include "common/typemaps.swg"
//%extern "engine/crefine.swg"
%extern "engine/cskeletonmodifier.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/crelaxrefine.h"
//#include "engine/crefine.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonmodifier.h"
%}

%pragma(python) include="engine/crelaxrefine.spy"

//%pragma(python) code="from ooflib.SWIG.engine.crefine import RefinePtr"
//%pragma(python) code="from ooflib.SWIG.engine.crefinementcriterion import RefinementTargets"
//%pragma(python) code="from ooflib.SWIG.engine.crefinementcriterion import RefinementCriterion"
%pragma(python) code = "from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierBasePtr, CSkeletonModifierPtr"

%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkelModCriterionPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeleton2 import CDeputySkeletonPtr"



class RelaxRefine : public CSkeletonModifier {
public:
RelaxRefine();

};




#endif 
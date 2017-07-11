// -*- C++ -*-

#include <oofconfig.h>

#ifndef CRELAXREFINE_H
#define CRELAXREFINE_H

#include "engine/cskeleton2_i.h"
#include "engine/crefine.h"

//Not actually sure what to inherit from yet

class RelaxRefine : public CSkeletonModifier {
 public:
  RelaxRefine();
  virtual ~RelaxRefine();

  CSkeletonBase* apply(CSkeletonBase* skeleton);
};


#endif //CRELAXREFINE_H

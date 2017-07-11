// -*- C++ -*-

//includes copied from csnaprefine
#include "common/IO/oofcerr.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/random.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonnode2.h"
#include "engine/crelaxrefine.h"
#include <vtkMath.h>

#include <algorithm>


CSkeletonBase* RelaxRefine::apply(CSkeletonBase* skeleton){
  std::cout << "This is the relaxrefine apply function" << std::endl;
  CSkeletonBase *copy = skeleton->deputyCopy();
  return copy;
}

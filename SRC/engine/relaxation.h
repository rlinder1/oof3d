//All includes are copied straight from cfiddlenodes
#include <oofconfig.h>


#ifndef RELAXATION_H
#define RELAXATION_H

#include "common/coord_i.h"
#include "engine/cskeletonselectable_i.h"
#include "engine/cskeletonmodifier.h"

//Not sure whether to inherit from fiddlenodes, skeleton modifier, or both


class Relax : public CSkeletonModifier {
protected:
  double alpha; //set by user
  double gamma; //set by user
  int iterations; //set by user

  char* materialName; //set to "boneMarrow" in constructor
  int count; //set to 0 in constructor
  bool solverConverged; //set to "true" in constructor
  char* meshName; //set to empty string in constructor
  double skelRelRate;
  //something about parameter name issues that I need to fix?
  int stiffness; //not actually an int
  //DirichletBC leftBoundaryCondition;
  int leftBoundaryCondition;
  int rightBoundaryCondition;
  int topBoundaryCondition;
  int bottomBoundaryCondition;
  int frontBoundaryCondition;
  int backBoundaryCondition;
  
 public:
  Relax(double alpha, double gamma, int iterations);
  virtual ~Relax();
 
 
  CSkeletonBase* apply(CSkeletonBase* skeleton);
  void updateNodePositionsC(CDeputySkeleton* skeleton, FEMesh* mesh);
  double getAlpha() {return alpha;}
  double getGamma() {return gamma;}
  int getIterations() {return iterations;}
  
};




#endif //RELAXATION_H

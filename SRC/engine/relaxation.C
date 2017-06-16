// -*- C++ -*-

//All includes copied directly from cfiddlenodes.C
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/random.h"
#include "common/progress.h"
#include "common/tostring.h"
#include "common/IO/oofcerr.h"
#include "engine/cfiddlenodes.h"
#include "engine/femesh.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/element.h"
#include "engine/node.h"
#include <algorithm>

//Except these
#include "engine/relaxation.h"
#include "engine/property/elasticity/iso/iso.h"
#include "engine/field.h"

Relax::Relax(double alpha, double gamma, int iterations)
  :alpha(alpha), gamma(gamma),
   iterations(iterations),
   count(0), solverConverged(true)
{}

Relax::~Relax() {}


CSkeletonBase* Relax::apply(CSkeletonBase *skeleton){
  std::cout << "Relax::apply has been called" << std::endl;
  CSkeletonBase *copy = skeleton->deputyCopy();
  return copy;
}

//confirm that this should take a deputy skeleton
void Relax::updateNodePositionsC(CDeputySkeleton* skeleton, FEMesh* mesh) {
  
  Field* displacement = Field::getField("Displacement");
  int numNodes = skeleton->nnodes();
  for (int i = 0; i < numNodes; i++) { 
    CSkeletonNode* node = skeleton->getNode(i);
    CSkeletonElementVector neighbors;
    node->getElements(skeleton, neighbors);
    CSkeletonElement* skelel = neighbors[0];
    
    Element* realel = mesh->getElement(skelel->getIndex());
    PointData* realnode = realel->getCornerFuncNode(skelel->getNodeIndexIntoList(node));
    double dx = displacement->value(mesh, realnode, 0);
    double dy = displacement->value(mesh, realnode, 1);
    double dz = displacement->value(mesh, realnode, 2);
    
    skeleton->moveNodeBy(node, Coord(dx, dy, dz));
  }
  
  
}

// -*- C++ -*-
// $RCSfile: thermo.swg,v $
// $Revision: 1.15.18.3 $
// $Author: fyc $
// $Date: 2014/07/29 21:22:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

%module thermo

%{
#include "engine/property/elasticity/thermo/thermo.h"
%}

%include "engine/typemaps.swg"
%include "engine/propertyhdr.swg"
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.cijkl import CijklPtr"
%extern "engine/property/elasticity/cijkl.swg"


// Typemap for conversion between the parameter type
// (IsotropicModulus) and the internal type, which is the swig'd Cijkl
// object from engine/property/elasticity/cijkl.h"
// TODO 3.1: Why does this have an explicit typemap?  Elasticity
// doesn't.  This should use the same mechanism as Elasticity.

%typemap(python,in) Cijkl * {
  PyObject *basevalue = PyObject_CallMethod($source, (char *) "to_base",NULL);
  
  PyObject *c11_float = PyObject_GetAttrString(basevalue,"c11");
  PyObject *c12_float = PyObject_GetAttrString(basevalue,"c12");

  double c11 = PyFloat_AsDouble(c11_float);
  double c12 = PyFloat_AsDouble(c12_float);

  Py_DECREF(c11_float);
  Py_DECREF(c12_float);

  $target = new Cijkl;
  (*$target)(0,0) = (*$target)(1,1) = (*$target)(2,2) = c11;
  (*$target)(0,1) = (*$target)(0,2) = (*$target)(1,2) = c12;
  (*$target)(3,3) = (*$target)(4,4) = (*$target)(5,5) = 0.5*(c11-c12);

}

%typemap(python,freearg) Cijkl * {
  delete $source;
}

%include "common/typemaps.swg"
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.elasticity import ElasticityPtr"
%extern "engine/property/elasticity/elasticity.swg"

class ThermoElasticityProp : public Elasticity {
public:
  ThermoElasticityProp(PyObject *, char *, Cijkl *cijkl,
		       double t0, double dmudt);
};


%pragma(python) include="thermo.spy"

%typemap(python,in) Cijkl* {}
%typemap(Python,freearg) Cijkl *{}

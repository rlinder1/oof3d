# -*- python -*-
# $RCSfile: DIR.py,v $
# $Revision: 1.4.18.1 $
# $Author: langer $
# $Date: 2013/11/08 20:45:21 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname   = 'color'
if not DIM_3:
    clib = 'oof2engine'
else:
    clib = 'oof3dengine'
cfiles    = ['color.C']
hfiles    = ['color.h']
swigfiles = ['color.swg']
swigpyfiles   = ['color.spy']


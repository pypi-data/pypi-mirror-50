#include <Python.h>
#include <numpy/arrayobject.h>
#include "thermal.h"

static char module_docstring[] =
    "sbpy sub-module to calculate thermal model surface temperature distributions.";
static char integrate_planck_docstring[] =
  "Romberg Integrator for thermal model Planck function integration in one dimension\n\nThis function is not intended for use by the sbpy user; based on 'Numerical Recipes in C', Press et al. 1988, Cambridge University Press.\n\nParameters\n----------\nmodel : int\n    model integrand identifier (1: STM, 2: FRM, 3: NEATM)\na : float\n    lower boundary for integration (radians)\nb : float\n    upper boundary for integration (radians)\nwavelengths : iterable of floats\n    wavelengths at which to evaluate integral (micron)\nT0 : float\n    subsolar temperature (K)\nphaseangle : float\n    solar phase angle (radians, only relevant for NEATM)\n\nReturns\n-------\nlist : values of the integral at provided wavelengths\n";

static PyObject *thermal_integrate_planck(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"integrate_planck", thermal_integrate_planck,
     METH_VARARGS, integrate_planck_docstring},
    {NULL, NULL, 0, NULL}
};

/* --------------------------- Module Interface -------------------------------- */

PyMODINIT_FUNC PyInit__thermal(void)
{
    
    PyObject *module;
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_thermal",
        module_docstring,
        -1,
        module_methods,
        NULL,
        NULL,
        NULL,
        NULL
    };
    module = PyModule_Create(&moduledef);
    if (!module) return NULL;

    /* Load `numpy` functionality. */
    import_array();
    
    return module;
}

/* ----------------------------- Integrator Interface -------------------------- */

static PyObject *thermal_integrate_planck(PyObject *self, PyObject *args)
{
  int model;
  double a, b, T0, phaseangle;
  PyObject *wavelengths_obj;

 
  /* Parse the input tuple */
  if (!PyArg_ParseTuple(args, "iddOdd", &model, &a, &b, &wavelengths_obj, &T0,
			&phaseangle))
        return NULL;

  PyObject *wavelengths_array = PyArray_FROM_OTF(wavelengths_obj, NPY_DOUBLE,
						 NPY_IN_ARRAY);

  /* If that didn't work, throw an exception. */
  if (wavelengths_array == NULL) {
    Py_XDECREF(wavelengths_array);
    return NULL;
  }

  /* extract number of wavelengths provided */
  int n_wavelengths = (int)PyArray_DIM(wavelengths_array, 0);
  
  /* extract wavelengths into c array */
  double *wavelengths = (double*)PyArray_DATA(wavelengths_array);
 
  /* Call the integrator for each wavelength and append results to a list*/
  PyObject* resultslist = PyList_New(0);
  int i;
  for (i=0; i<n_wavelengths; i++) {
    double wavelength = wavelengths[i];
    double value = integrate_planck(model, a, b, wavelength, T0, phaseangle);
    
    /* Resolve error codes */
    switch ((int)value) {
    case -9999: 
      PyErr_SetString(PyExc_RuntimeError,
		      "Temperature distribution integration did not converge.");
      return NULL;
      break;
    case -9998:
      PyErr_SetString(PyExc_RuntimeError,
		      "Temperature distribution integration returned NaN.");
      return NULL;
      break;
    }

    // append value to resultslist
    PyList_Append(resultslist, Py_BuildValue("d", value)); 
  }

  /* Clean up. */
  Py_DECREF(wavelengths_array);
  
  return resultslist;
}

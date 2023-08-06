====
ellc
====

Generate light curves or radial velocity curves for a binary
star system with the ellc light curve model. [1]_

Installation of this module requires python 3.x and numpy. The anaconda
distribution of python3 is recommended.

To install this module on linux-like systems run the following command
$ pip install ellc
or to install on your system if you have root access
$ sudo pip install ellc

Mac OSX - you may need to add a symbolic link so that pip can find the
correct version of gfortran, e.g., for macports users ...
 $ ln -s /opt/local/bin/gfortran-mp-6  /opt/local/bin/gfortran  

Routines in this module:

  lc(t_obs, radius_1, radius_2, sbratio, incl, ... ) 

  rv(t_obs, radius_1, radius_2, sbratio, incl, t_zero, period, a, q, ...)

  fluxes(t_obs, radius_1, radius_2, sbratio, incl, ... ) 
  
  ldy.LimbGravityDarkeningCoeffs()

Documentation and examples for each routine are included in the file headers
and can be viewed from within python in the normal way, e.g., 
 >>> import ellc
 >>> print(ellc.ldy.__doc__)

The easiest way to fit a single light curve is use ellc_emcee (you will need
to add the appropriate /bin/ directory to your path). Run the command
ellc_emcee and follow the prompts. You can grab the output from this script in
the log file and use this as the basis of a new input file for this script.
Use ./ellc_emcee.py -h to see command-line options.

Please cite Maxted (2016) if you published results based on this software.
See sub-directory examples/ for scripts used to generate the figures in this
paper. 

.. rubric:: References
.. [1] Maxted, P.F.L. 2016. A fast, flexible light curve model for detached
   eclipsing binary stars and transiting exoplanets. A&A 591, A111

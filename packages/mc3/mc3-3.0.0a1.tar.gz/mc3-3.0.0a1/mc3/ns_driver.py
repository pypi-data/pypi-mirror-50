# Copyright (c) 2015-2019 Patricio Cubillos and contributors.
# MC3 is open-source software under the MIT license (see LICENSE).

__all__ = ["nested_sampling"]

import os
import sys
import importlib
from datetime import date

if sys.version_info.major == 2:
    range = xrange

import numpy as np
import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
    mpl.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mpr
from pathos.multiprocessing import ProcessingPool

from .fit_driver import fit
from . import utils   as mu
from . import plots   as mp
from . import stats   as ms
from .VERSION import __version__


@mu.ignore_system_exit
def nested_sampling(data=None,     uncert=None,
    func=None,     params=None,    indparams=[],
    pmin=None,     pmax=None,      pstep=None,
    prior=None,    priorlow=None,  priorup=None,
    ncpu=1,        nsamples=None,
    sampler=None,
    leastsq=None,   chisqscale=False,
    thinning=1,
    plots=False,   ioff=False,     showbp=True,
    savefile=None,
    resume=False,
    rms=False,     log=None,
    pnames=None,   texnames=None,
    ):
  """
  This beautiful piece of code runs a Markov-chain Monte Carlo algorithm.

  Parameters
  ----------
  data: 1D float ndarray or string
      Data to be fit by func.  If string, path to file containing data.
  uncert: 1D float ndarray
      Uncertainties of data.
  func: Callable or string-iterable
      The callable function that models data as:
          model = func(params, *indparams)
      Or an iterable of 3 strings (funcname, modulename, path)
      that specifies the function name, function module, and module path.
      If the module is already in the python-path scope, path can be omitted.
  indparams: tuple or string
      Additional arguments required by func.  If string, path to file
      containing indparams.
  params: 1D/2D float ndarray or string
      Set of initial fitting parameters for func.  If 2D, of shape
      (nparams, nchains), it is assumed that it is one set for each chain.
      If string, path to file containing data.
  pmin: 1D ndarray
      Lower boundaries for the posterior exploration.
  pmax: 1D ndarray
      Upper boundaries for the posterior exploration.
  pstep: 1D ndarray
      Parameter stepping.  If a value is 0, keep the parameter fixed.
      Negative values indicate a shared parameter (See Note 1).
  prior: 1D ndarray
      Parameter prior distribution means (See Note 2).
  priorlow: 1D ndarray
      Lower prior uncertainty values (See Note 2).
  priorup: 1D ndarray
      Upper prior uncertainty values (See Note 2).
  nchains: Scalar
      Number of simultaneous chains to run.
  ncpu: Integer
      Number of processors for the MCMC chains (MC3 defaults to
      one CPU for each chain plus a CPU for the central hub).
  nsamples: Scalar
      Total number of samples.
  sampler: String
      Sampler algorithm:
      - 'mrw':  Metropolis random walk.
      - 'demc': Differential Evolution Markov chain.
      - 'snooker': DEMC-z with snooker update.
  wlike: Bool
      If True, calculate the likelihood in a wavelet-base.  This requires
      three additional parameters (See Note 3).
  leastsq: String
      If not None, perform a least-square optimization before the MCMC run.
      Select from:
          'lm':  Levenberg-Marquardt (most efficient, but does not obey bounds)
          'trf': Trust Region Reflective
  chisqscale: Boolean
      Scale the data uncertainties such that the reduced chi-squared = 1.
  grtest: Boolean
      Run Gelman & Rubin test.
  grbreak: Float
      Gelman-Rubin convergence threshold to stop the MCMC (I'd suggest
      grbreak ~ 1.001--1.005).  Do not break if grbreak=0.0 (default).
  grnmin: Integer or float
      Minimum number of samples required for grbreak to stop the MCMC.
      If grnmin > 1: grnmin sets the minimum required number of samples.
      If 0 < grnmin < 1: grnmin sets the minimum required nsamples fraction.
  burnin: Integer
      Number of burned-in (discarded) number of iterations at the beginning
      of the chains.
  thinning: Integer
      Thinning factor of the chains (use every thinning-th iteration) used
      in the GR test and plots.
  fgamma: Float
      Proposals jump scale factor for DEMC's gamma.
      The code computes: gamma = fgamma * 2.38 / sqrt(2*Nfree)
  fepsilon: Float
      Jump scale factor for DEMC's support distribution.
      The code computes: e = fepsilon * Normal(0, pstep)
  hsize: Integer
      Number of initial samples per chain.
  kickoff: String
      Flag to indicate how to start the chains:
      'normal' for normal distribution around initial guess, or
      'uniform' for uniform distribution withing the given boundaries.
  plots: Bool
      If True plot parameter traces, pairwise-posteriors, and posterior
      histograms.
  ioff: Bool
      If True, set plt.ioff(), i.e., do not display figures on screen.
  showbp: Bool
      If True, show best-fitting values in histogram and pairwise plots.
  savefile: String
      If not None, filename to store allparams and other MCMC results.
  resume: Boolean
      If True resume a previous run.
  rms: Boolean
      If True, calculate the RMS of the residuals: data - best_model.
  log: String or FILE pointer
      Filename or File object to write log.
  pnames: 1D string iterable
      List of parameter names (including fixed and shared parameters)
      to display on output screen and figures.  See also texnames.
      Screen output trims up to the 11th character.
      If not defined, default to texnames.
  texnames: 1D string iterable
      Parameter names for figures, which may use latex syntax.
      If not defined, default to pnames.

  Returns
  -------
  mc3_output: Dict
      A Dictionary containing the MCMC posterior distribution and related
      stats, including:
      - Z: thinned posterior distribution of shape [nsamples, nfree].
      - Zchain: chain indices for each sample in Z.
      - Zchisq: chi^2 value for each sample in Z.
      - Zmask: indices that turn Z into the desired posterior.
      - burnin: number of burned-in samples per chain.
      - CRlo: lower boundary of the marginal 68%-highest posterior
            density (the credible region).
      - CRhi: upper boundary of the marginal 68%-HPD.
      - stdp: standard deviation of the marginal posteriors.
      - meanp: mean of the marginal posteriors.
      - bestp: model parameters for the lowest-chi^2 sample.
      - best_chisq: lowest-chi^2 in the sample.
      - best_model: model evaluated at bestp.
      - red_chisq: reduced chi-squared: chi^2/(Ndata}-Nfree) for the
            best-fitting sample.
      - BIC: Bayesian Information Criterion: chi^2-Nfree log(Ndata)
            for the best-fitting sample.
      - chisq_factor: Uncertainties scale factor to enforce chi^2_red = 1.
      - stddev_residuals: standard deviation of the residuals.
      - acceptance_rate: sample's acceptance rate.

  Notes
  -----
  1.- To set one parameter equal to another, set its pstep to the
      negative index in params (Starting the count from 1); e.g.: to set
      the second parameter equal to the first one, do: pstep[1] = -1.
  2.- If any of the fitting parameters has a prior estimate, e.g.,
        param[i] = p0 +up/-low,
      with up and low the 1sigma uncertainties.  This information can be
      considered in the MCMC run by setting:
      prior[i]    = p0
      priorup[i]  = up
      priorlow[i] = low
      All three: prior, priorup, and priorlow must be set and, furthermore,
      priorup and priorlow must be > 0 to be considered as prior.
  3.- If data, uncert, params, pmin, pmax, pstep, prior, priorlow,
      or priorup are set as filenames, the file must contain one value per
      line.
      For simplicity, the data file can hold both data and uncert arrays.
      In this case, each line contains one value from each array per line,
      separated by an empty-space character.
      Similarly, params can hold: params, pmin, pmax, pstep, priorlow,
      and priorup.  The file can hold as few or as many array as long as
      they are provided in that exact order.
  4.- An indparams file works differently, the file will be interpreted
      as a list of arguments, one in each line.  If there is more than one
      element per line (empty-space separated), it will be interpreted as
      an array.
  5.- FINDME: WAVELET LIKELIHOOD

  Examples
  --------
  >>> # See https://mc3.readthedocs.io/en/latest/ns_tutorial.html

import numpy as np
import mc3

def quad(p, x):
    return p[0] + p[1]*x + p[2]*x**2.0

# Create a noisy synthetic dataset:
x = np.linspace(0, 10, 100)
p_true = [3, -2.4, 0.5]
y = quad(p_true, x)
uncert = np.sqrt(np.abs(y))
error = np.random.normal(0, uncert)
data = y + error

# Initial guess for fitting parameters:
params = np.array([3.0, -2.0, 0.1])
pstep  = np.array([0.0, 0.03, 0.05])
pmin   = np.array([ 0.0, -5.0, -1.0])
pmax   = np.array([20.0,  5.0,  1.0])

indparams = [x]
func = quad
ncpu = 4

mc3_results = mc3.nested_sampling(data, uncert, func=quad, params=params,
    indparams=[x], pstep=pstep, ncpu=ncpu, pmin=pmin, pmax=pmax, leastsq='lm')

mc3_mcmc = mc3.mcmc(data, uncert, func=quad, params=params, indparams=[x],
    pstep=pstep, ncpu=ncpu, pmin=pmin, pmax=pmax, leastsq='lm')
  """
  # Logging object:
  if isinstance(log, str):
      log = mu.Log(log, append=resume)
      closelog = True
  else:
      closelog = False
      if log is None:
          log = mu.Log()

  try:
      import dynesty
  except ModuleNotFoundError:
      log.error("ModuleNotFoundError: No module named 'dynesty'")

  log.msg("\n{:s}\n"
      "  Multi-core Markov-chain Monte Carlo (MC3).\n"
      "  Version {}.\n"
      "  Copyright (c) 2015-{:d} Patricio Cubillos and collaborators.\n"
      "  MC3 is open-source software under the MIT license (see LICENSE).\n"
      "{:s}\n\n".format(log.sep, __version__, date.today().year, log.sep))

  # Read the model parameters:
  params = mu.isfile(params, 'params', log, 'ascii', False, not_none=True)
  # Unpack if necessary:
  if np.ndim(params) > 1:
      ninfo, ndata = np.shape(params)
      if ninfo == 7:
          prior    = params[4]
          priorlow = params[5]
          priorup  = params[6]
      if ninfo >= 4:
          pstep    = params[3]
      if ninfo >= 2:
          pmin     = params[1]
          pmax     = params[2]
      else:
          log.error('Invalid format/shape for params input file.')
      params = params[0]

  # Process data and uncertainties:
  data = mu.isfile(data, 'data', log, 'bin', False, not_none=True)
  if np.ndim(data) > 1:
      data, uncert = data
  # Make local 'uncert' a copy, to avoid overwriting:
  if uncert is None:
      log.error("'uncert' is a required argument.")
  else:
      uncert = np.copy(uncert)

  # Process the independent parameters:
  if indparams != []:
      indparams = mu.isfile(indparams, 'indparams', log, 'bin', unpack=False)

  if ioff:
      plt.ioff()

  #if resume:
  #    log.msg("\n\n{:s}\n{:s}  Resuming previous MCMC run.\n\n".
  #            format(log.sep, log.sep))

  # Import the model function:
  if isinstance(func, (list, tuple, np.ndarray)):
      if len(func) == 3:
          sys.path.append(func[2])
      else:
          sys.path.append(os.getcwd())
      fmodule = importlib.import_module(func[1])
      func = getattr(fmodule, func[0])
  elif not callable(func):
      log.error("'func' must be either a callable or an iterable of strings "
                "with the model function, file, and path names.")

  # Cap the number of processors:
  if ncpu >= mpr.cpu_count():
      log.warning("The number of requested CPUs ({:d}) is >= than the number "
                  "of available CPUs ({:d}).  Enforced ncpu to {:d}.".
                 format(ncpu, mpr.cpu_count(), mpr.cpu_count()-1))
      ncpu = mpr.cpu_count() - 1

  nparams = len(params)
  ndata   = len(data)

  # Setup array of parameter names:
  if   pnames is None     and texnames is not None:
      pnames = texnames
  elif pnames is not None and texnames is None:
      texnames = pnames
  elif pnames is None     and texnames is None:
      pnames = texnames = mu.default_parnames(nparams)
  pnames   = np.asarray(pnames)
  texnames = np.asarray(texnames)

  if pmin is None or pmax is None:
      log.error('Parameter space must be constrained by pmin and pmax.')
  pmin = np.asarray(pmin)
  pmax = np.asarray(pmax)
  # Set default pstep:
  if pstep is None:
      pstep = 0.1 * np.abs(params)
  pstep = np.asarray(pstep)
  # Set prior parameter indices:
  if prior is None or priorup is None or priorlow is None:
      prior = priorup = priorlow = np.zeros(nparams)

  # Check that initial values lie within the boundaries:
  if (np.any(np.asarray(params) < pmin)
   or np.any(np.asarray(params) > pmax)):
      pout = ""
      for pname, par, minp, maxp in zip(pnames, params, pmin, pmax):
          if par < minp:
              pout += "\n{:11s}  {: 12.5e} < {: 12.5e}".format(
                  pname[:11], minp, par)
          if par > maxp:
              pout += "\n{:26s}  {: 12.5e} > {: 12.5e}".format(
                  pname[:11], par, maxp)

      log.error("Some initial-guess values are out of bounds:\n"
                "Param name           pmin          value           pmax\n"
                "-----------  ------------   ------------   ------------"
                "{:s}".format(pout))

  nfree  = int(np.sum(pstep > 0))   # Number of free parameters
  ifree  = np.where(pstep > 0)[0]   # Free   parameter indices
  ishare = np.where(pstep < 0)[0]   # Shared parameter indices

  # Check that output path exists:
  if savefile is not None:
      fpath, fname = os.path.split(os.path.realpath(savefile))
      if not os.path.exists(fpath):
          log.warning("Output folder path: '{:s}' does not exist. "
                      "Creating new folder.".format(fpath))
          os.makedirs(fpath)

  # Least-squares minimization:
  if leastsq is not None:
      fitpars = np.asarray(params)
      fit_output = fit(fitpars, func, data, uncert, indparams,
          pstep, pmin, pmax, prior, priorlow, priorup, leastsq)
      log.msg("Least-squares best-fitting parameters:\n  {:s}\n\n".
               format(str(fit_output['bestp'])), si=2)

  # Scale data-uncertainties such that reduced chisq = 1:
  chisq_factor = 1.0
  # TBD: This only makes sense if leastsq is not None:
  if chisqscale:
      chisq_factor = np.sqrt(fit_output['chisq']/(ndata-nfree))
      uncert *= chisq_factor

      # Re-calculate best-fitting parameters with new uncertainties:
      if leastsq is not None:
          fit_output = fit(fitpars, func, data, uncert, indparams,
              pstep, pmin, pmax, prior, priorlow, priorup, leastsq)
          log.msg("Least-squares best-fitting parameters (rescaled chisq):"
                  "\n  {:s}\n\n".format(str(fit_output['bestp'])), si=2)

  # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
  # Nested-Sampling:
  # can't use multiprocessing.Pool since map can't pickle defs:
  pool = ProcessingPool(nodes=ncpu) if ncpu > 1 else None
  queue_size = ncpu if ncpu > 1 else None

  # Setup prior transform:
  priors = []
  for p0, plo, pup, min, max, step in zip(prior, priorlow, priorup,
          pmin, pmax, pstep):
      if step <= 0:
          continue
      if plo == 0.0 and pup == 0.0:
          priors.append(ms.ppf_uniform(min, max))
      else:
          priors.append(ms.ppf_gaussian(p0, plo, pup))

  def prior_trans(u):
      return [prior(v) for v,prior in zip(u,priors)]

  def loglike(pars):
      params[ifree] = pars
      for s in ishare:
          params[s] = params[-int(pstep[s])-1]
      return -0.5*np.sum((data-func(params, *indparams))**2/uncert**2)

  #sampler = dynesty.DynamicNestedSampler(
  sampler = dynesty.NestedSampler(
      loglike,
      prior_trans,
      nfree,
      #nlive=1500,
      #first_update={'min_ncall': 5000, 'min_eff': 50.},
      pool=pool,
      queue_size=queue_size,
      )
  sampler.run_nested()

  samples = sampler.results.samples
  weights = np.exp(sampler.results.logwt - sampler.results.logz[-1])
  posterior = dynesty.utils.resample_equal(samples, weights)
  bestp = np.copy(params)
  bestp[ifree] = sampler.results['samples'][np.argmax(sampler.results['logl'])]

  # Evaluate model for best fitting parameters:
  for s in ishare:
      bestp[s] = bestp[-int(pstep[s])-1]
  best_model = func(bestp, *indparams)
  best_chisq = -2.0*np.amax(sampler.results['logl'])

  chisq = ms.chisq(best_model, data, uncert, params, prior, priorlow, priorup)
  print(f"FIT = {fit_output['chisq']}\nDYN = {best_chisq}\nNS  = {chisq}")

  if leastsq is not None and best_chisq-fit_output['chisq'] < -3.0e-8:
      with np.printoptions(precision=8):
          log.warning(
              "MCMC found a better fit than the minimizer:\n"
              "MCMC best-fitting parameters:        (chisq={:.8g})\n{:s}\n"
              "Minimizer best-fitting parameters:   (chisq={:.8g})\n"
              "{:s}".format(best_chisq, str(bestp),
                            fit_output['chisq'], str(fit_output['bestp'])))

  if leastsq is not None:
      chisq = fit_output['chisq']

  # Print out Summary:
  log.msg("\nNested Sampling Summary:"
          "\n------------------------")
  # Truncate sample (if necessary):
  Zchisq = -2.0*sampler.results['logl']

  # Get some stats:
  nsample  = sampler.results['niter']
  nZsample = len(posterior)  # Valid samples (after thinning and burning)
  BIC      = chisq + nfree*np.log(ndata)
  if ndata > nfree:
      red_chisq = chisq/(ndata-nfree)
  else:
      red_chisq = np.nan
  sdr = np.std(best_model-data)

  fmt = len(str(nsample))
  log.msg("Total number of samples:            {:{}d}".
          format(nsample,  fmt), indent=2)
  #log.msg("Number of parallel chains:          {:{}d}".
  #        format(nchains,  fmt), indent=2)
  log.msg("Thinning factor:                    {:{}d}".
          format(thinning, fmt), indent=2)
  log.msg("NS sample size (thinned): {:{}d}".
          format(nZsample, fmt), indent=2)
  log.msg("Sampling efficiency:   {:.2f}%\n".
          format(sampler.results['eff']), indent=2)

  # Compute the credible region for each parameter:
  CRlo = np.zeros(nparams)
  CRhi = np.zeros(nparams)
  pdf  = []
  xpdf = []
  for post, idx in zip(posterior.T, ifree):
  #for i in range(nfree):
      #PDF, Xpdf, HPDmin = ms.cred_region(posterior[:,i])
      PDF, Xpdf, HPDmin = ms.cred_region(post)
      pdf.append(PDF)
      xpdf.append(Xpdf)
      #CRlo[ifree[i]] = np.amin(Xpdf[PDF>HPDmin])
      #CRhi[ifree[i]] = np.amax(Xpdf[PDF>HPDmin])
      CRlo[idx] = np.amin(Xpdf[PDF>HPDmin])
      CRhi[idx] = np.amax(Xpdf[PDF>HPDmin])
  # CR relative to the best-fitting value:
  CRlo[ifree] -= bestp[ifree]
  CRhi[ifree] -= bestp[ifree]

  # Get the mean and standard deviation from the posterior:
  meanp = np.zeros(nparams, np.double) # Parameters mean
  stdp  = np.zeros(nparams, np.double) # Parameter standard deviation
  meanp[ifree] = np.mean(posterior, axis=0)
  stdp [ifree] = np.std(posterior,  axis=0)
  for s in ishare:
      bestp[s] = bestp[-int(pstep[s])-1]
      meanp[s] = meanp[-int(pstep[s])-1]
      stdp [s] = stdp [-int(pstep[s])-1]
      CRlo [s] = CRlo [-int(pstep[s])-1]
      CRhi [s] = CRhi [-int(pstep[s])-1]

  log.msg("\nParam name     Best fit   Lo HPD CR   Hi HPD CR        Mean    Std dev       S/N"
          "\n----------- ----------------------------------- ---------------------- ---------", width=80)
  for i in range(nparams):
      snr  = "{:.1f}".   format(np.abs(bestp[i])/stdp[i])
      mean = "{: 11.4e}".format(meanp[i])
      lo   = "{: 11.4e}".format(CRlo[i])
      hi   = "{: 11.4e}".format(CRhi[i])
      if   i in ifree:  # Free-fitting value
          pass
      elif i in ishare: # Shared value
          snr = "[share{:02d}]".format(-int(pstep[i]))
      else:             # Fixed value
          snr = "[fixed]"
          mean = "{: 11.4e}".format(bestp[i])
      log.msg("{:<11s} {:11.4e} {:>11s} {:>11s} {:>11s} {:10.4e} {:>9s}".
              format(pnames[i][0:11], bestp[i], lo, hi, mean, stdp[i], snr),
              width=160)

  fmt = len("{:.4f}".format(BIC))  # Length of string formatting
  log.msg(" ")
  if chisqscale:
      log.msg("sqrt(reduced chi-squared) factor: {:{}.4f}".
              format(chisq_factor, fmt), indent=2)
  log.msg("Best-parameter's chi-squared:     {:{}.4f}".
          format(chisq, fmt), indent=2)
  log.msg("Bayesian Information Criterion:   {:{}.4f}".
          format(BIC, fmt), indent=2)
  log.msg("Reduced chi-squared:              {:{}.4f}".
          format(red_chisq, fmt), indent=2)
  log.msg("Standard deviation of residuals:  {:.6g}\n".format(sdr), indent=2)

  if savefile is not None or plots or closelog:
      log.msg("\nOutput MCMC files:")

  # Build the output dict:
  output = {
      'bestp':bestp,
      'meanp':meanp,
      'stdp':stdp,
      'CRlo':CRlo,
      'CRhi':CRhi,
      'stddev_residuals':sdr,
      'Z':posterior,
      'Zchisq':Zchisq,
      'best_model':best_model,
      'best_chisq':chisq,
      'red_chisq':red_chisq,
      'chisq_factor':chisq_factor,
      'BIC':BIC,
      'eff':sampler.results['eff'],
      }

  # Save definitive results:
  if savefile is not None:
      np.savez(savefile, **output)
      log.msg("'{:s}'".format(savefile), indent=2)

  if rms:
      RMS, RMSlo, RMShi, stderr, bs = ms.time_avg(best_model-data)

  if plots:
      # Extract filename from savefile:
      if savefile is not None:
          if savefile.rfind(".") == -1:
              fname = savefile
          else:
              # Cut out file extention.
              fname = savefile[:savefile.rfind(".")]
      else:
          fname = 'NS'
      # Include bestp in posterior plots:
      best_freepars = bestp[ifree] if showbp else None
      # Trace plot:
      mp.trace(posterior, Zchain=None, burnin=0, pnames=texnames[ifree],
          savefile=fname+"_trace.png")
      log.msg("'{:s}'".format(fname+"_trace.png"), indent=2)
      # Pairwise posteriors:
      mp.pairwise(posterior,  pnames=texnames[ifree], bestp=best_freepars,
          savefile=fname+"_pairwise.png")
      #axes, cb = mp.pairwise(posterior, pnames=texnames, bestp=bestp)
      log.msg("'{:s}'".format(fname+"_pairwise.png"), indent=2)
      # Histograms:
      mp.histogram(posterior, pnames=texnames[ifree], bestp=best_freepars,
          savefile=fname+"_posterior.png",
          percentile=0.683, pdf=pdf, xpdf=xpdf)
      log.msg("'{:s}'".format(fname+"_posterior.png"), indent=2)
      # RMS vs bin size:
      if rms:
          mp.rms(bs, RMS, stderr, RMSlo, RMShi, binstep=len(bs)//500+1,
                 savefile=fname+"_RMS.png")
          log.msg("'{:s}'".format(fname+"_RMS.png"), indent=2)
      # Sort of guessing that indparams[0] is the X array for data as in y=y(x):
      if (indparams != []
          and isinstance(indparams[0], (list, tuple, np.ndarray))
          and np.size(indparams[0]) == ndata):
          try:
              mp.modelfit(data, uncert, indparams[0], best_model,
                          savefile=fname+"_model.png")
              log.msg("'{:s}'".format(fname+"_model.png"), indent=2)
          except:
              pass

  # Close the log file if necessary:
  if closelog:
      log.msg("'{:s}'".format(log.logname), indent=2)
      log.close()

  return output

# Copyright (c) 2015-2019 Patricio Cubillos and contributors.
# MC3 is open-source software under the MIT license (see LICENSE).

from .mcmc_driver import *
from .ns_driver import *
from .fit_driver import *
from . import plots
from . import utils
from . import stats
from . import rednoise
from .VERSION import __version__


__all__ = (
    mcmc_driver.__all__
  + ns_driver.__all__
  + fit_driver.__all__
  + ['plots', 'utils', 'stats', 'rednoise']
    )


# Clean up top-level namespace--delete everything that isn't in __all__
# or is a magic attribute, and that isn't a submodule of this package
for varname in dir():
    if not ((varname.startswith('__') and varname.endswith('__')) or
            varname in __all__):
        del locals()[varname]
del(varname)
